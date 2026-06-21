---
title: Domain: E-commerce, Legal, and HR Agents
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, domains, ecommerce, legal, hr, case-studies]
confidence: high
source_files: 3
---

# Domain: E-commerce, Legal, and HR Agents

> Consolidated from 3 source files.

---

## E-commerce / Retail: Agents at Billion-User Scale

## Domain Constraints

E-commerce is ruthless about economics. An agent that's 1% slower or 1% more expensive scales into millions of wasted dollars per day.

**The immutable constraints:**

- **Latency is revenue.** Every 100ms slower = measurable conversion loss. Agents must respond in <100ms for consumer-facing features, often <10ms for backend.
- **Scale is existential.** DoorDash runs over 10M products. Amazon sees 2B transactions daily. Your agent must work at that scale or it doesn't matter.
- **Personalization without privacy invasion.** Show the right product to the right person, but don't feel creepy. GDPR compliance at scale.
- **Wrong recommendations cost money.** Showing a $500 item to someone shopping for $20 groceries wastes their time and your ad budget. Precision matters.

---

## Architecture Focus

The pattern across e-commerce companies isn't "smarter recommenders". It's **multi-tier agents with latency budgets**.

```
Request arrives
│
├─ Tier 1 (cache, <5ms)
│  ├─ Recent searches?
│  ├─ Seasonal products?
│  └─ Global top sellers?
│
├─ Tier 2 (personalization, <50ms)
│  ├─ User embeddings (precomputed)
│  ├─ Quick product filtering
│  └─ Reranking with lightweight model
│
├─ Tier 3 (deep reasoning, <500ms)
│  ├─ Multi-turn orchestration
│  ├─ Heavy computation
│  └─ User feedback loops
│
└─ Response
   (if Tier 1 & 2 fail, return default)
```

**Key insight:** Multi-tier is not a fallback; it's the primary architecture. Tier 1 satisfies 95% of cases. Tiers 2-3 handle the complex 5%.

---

## Case Studies: Architecture + Design Decisions

### 1. DoorDash — Personalization Over 10M+ Products

**The Problem:** DoorDash's catalog is massive: 10M+ restaurants, each with 50-500 menu items. Recommending the "right" item per user per context (time of day, location, mood, budget) requires understanding billions of combinations.

**Architecture Decision:**

```python
# DoorDash's multi-tier recommendation pattern

from dataclasses import dataclass
from enum import Enum

class RecommendationTier(Enum):
    CACHE = 0          # Pre-computed, <5ms
    PERSONALIZED = 1   # Real-time embeddings, <50ms
    REASONING = 2      # Full agent reasoning, <500ms

@dataclass
class RecommendationContext:
    user_id: str
    location: tuple  # (lat, lon)
    time_of_day: str  # "breakfast", "lunch", "dinner", "late_night"
    cuisine_preference: str
    price_range: str
    delivery_time_willing_to_wait: int  # minutes

class DoorDashRecommendationAgent:
    """Multi-tier recommendation: fast by default"""
    
    async def get_recommendations(
        self,
        context: RecommendationContext,
        timeout_ms: int = 100
    ) -> list[dict]:
        """Get recommendations within latency budget"""
        
        start_time = time.time_ns()
        
        # Tier 1: Cache (use all budget?)
        tier1_results = await self._tier1_cache(context)
        if tier1_results and time.time_ns() - start_time < 5_000_000:  # 5ms
            return tier1_results
        
        # Tier 2: Personalization (50ms budget)
        tier2_results = await self._tier2_personalized(
            context,
            timeout_ms=min(50, timeout_ms - elapsed_ms(start_time))
        )
        if tier2_results:
            return tier2_results
        
        # Tier 3: Reasoning (remaining budget)
        tier3_results = await self._tier3_reasoning(
            context,
            timeout_ms=timeout_ms - elapsed_ms(start_time)
        )
        if tier3_results:
            return tier3_results
        
        # Fallback
        return await self._fallback_recommendations(context)
    
    async def _tier1_cache(self, context: RecommendationContext) -> list[dict]:
        """Pre-computed recommendations: very fast"""
        
        # Cache keys: by (location, time_of_day, price_range)
        cache_key = f"{context.location}|{context.time_of_day}|{context.price_range}"
        
        # Redis lookup
        cached = await self.redis.get(cache_key)
        
        if cached:
            # Return, but shuffle order per user (personalization)
            results = json.loads(cached)
            
            # Light personalization: reorder by user's preference
            user_pref = await self._get_user_cuisine_preference(context.user_id)
            results = self._reorder_by_preference(results, user_pref)
            
            return results
        
        return None
    
    async def _tier2_personalized(
        self,
        context: RecommendationContext,
        timeout_ms: int
    ) -> list[dict]:
        """Real-time personalization with embeddings"""
        
        # Step 1: Get user embedding (precomputed)
        user_emb = await self._get_user_embedding(context.user_id)
        
        # Step 2: Get candidates (fast ANN search)
        # "Find restaurants similar to user's embedding"
        candidate_restaurants = await self._ann_search(
            user_emb,
            limit=50,
            timeout_ms=20,
        )
        
        # Step 3: Quick reranking (lightweight model)
        ranked = await self._rerank_fast(
            candidate_restaurants,
            context,
            timeout_ms=20,
        )
        
        # Step 4: Expand to items
        results = []
        for restaurant in ranked[:5]:
            items = await self._get_top_items_for_restaurant(
                restaurant.id,
                context.user_id,
            )
            results.extend(items)
        
        return results[:10]
    
    async def _tier3_reasoning(
        self,
        context: RecommendationContext,
        timeout_ms: int
    ) -> list[dict]:
        """Full agent reasoning (expensive, only if needed)"""
        
        # Expensive operations:
        # - Multi-turn reasoning
        # - Why does user like cuisines?
        # - What's the occasion?
        # - What's user's mood?
        
        # Only run if Tier 2 failed or user is premium
        if not context.user_id.startswith("premium"):
            return None  # Don't waste budget
        
        reasoning = {
            "what_is_user_craving": await self._infer_craving(context),
            "what_restaurants_match": await self._find_matching_restaurants(
                context,
                timeout_ms=timeout_ms
            ),
            "what_items_per_restaurant": await self._select_items(context),
        }
        
        results = []
        for restaurant in reasoning["what_restaurants_match"][:3]:
            items = reasoning["what_items_per_restaurant"].get(restaurant.id, [])
            results.extend(items)
        
        return results[:10]
    
    async def _ann_search(
        self,
        user_embedding: list[float],
        limit: int,
        timeout_ms: int
    ) -> list[dict]:
        """Approximate Nearest Neighbor search"""
        
        # FAISS or equivalent: find similar restaurants
        # This is fast because embeddings are pre-computed
        
        # Query: "Find 50 restaurants most similar to this user"
        candidates = await self.faiss.search(
            user_embedding,
            k=limit,
        )
        
        return candidates
    
    async def _rerank_fast(
        self,
        candidates: list[dict],
        context: RecommendationContext,
        timeout_ms: int
    ) -> list[dict]:
        """Lightweight reranking"""
        
        # Don't use a big model; use heuristics
        
        scored = []
        for candidate in candidates:
            score = 0
            
            # Signal 1: Distance from user
            distance = self._calc_distance(candidate.location, context.location)
            score += (1 - distance / 10000) * 0.3  # Closer = higher score
            
            # Signal 2: Estimated delivery time
            estimated_time = await self._estimate_delivery(candidate.id)
            if estimated_time <= context.delivery_time_willing_to_wait:
                score += 0.4
            
            # Signal 3: User has ordered from here before?
            if await self._user_has_ordered_from(context.user_id, candidate.id):
                score += 0.2
            
            # Signal 4: Cuisine match
            if candidate.cuisine == context.cuisine_preference:
                score += 0.1
            
            scored.append((candidate, score))
        
        # Return top-k by score
        ranked = sorted(scored, key=lambda x: -x[1])
        return [r[0] for r in ranked]

# Cache strategy
class CacheStrategy:
    """Pre-compute cache for Tier 1"""
    
    async def warm_cache(self):
        """Pre-compute popular recommendations"""
        
        # Identify popular contexts
        # Example: (NYC, lunch, under $20)
        
        popular_contexts = [
            ("40.7128,-74.0060", "lunch", "under_20"),  # NYC lunch budget
            ("40.7128,-74.0060", "dinner", "under_50"), # NYC dinner mid
            ("37.7749,-122.4194", "lunch", "under_15"), # SF lunch budget
            # ... 1000s more
        ]
        
        for location, time_of_day, price_range in popular_contexts:
            # Compute recommendations
            recommendations = await self._compute_for_context(
                location, time_of_day, price_range
            )
            
            # Cache for 1 hour
            await self.redis.set(
                f"{location}|{time_of_day}|{price_range}",
                json.dumps(recommendations),
                ex=3600
            )

# Economics
class DoorDashEconomics:
    def cost_per_recommendation(self):
        return {
            "tier_1": 0.00001,  # Cache hit: almost free
            "tier_2": 0.0001,   # ANN search + reranking: cheap
            "tier_3": 0.001,    # Full reasoning: expensive
        }
    
    def usage_distribution(self):
        # Realistic distribution
        return {
            "tier_1": 0.70,  # 70% cache hits
            "tier_2": 0.25,  # 25% real-time personalization
            "tier_3": 0.05,  # 5% deep reasoning
        }
    
    def average_cost(self):
        dist = self.usage_distribution()
        costs = self.cost_per_recommendation()
        
        return sum(
            dist[tier] * costs[tier]
            for tier in ["tier_1", "tier_2", "tier_3"]
        )

# 100M requests per day
# Average cost: $400/day (and growing slowly with scale)
# Per user cost (500M users): negligible
```

**Why This Works:**

- Tier 1 handles 70% of cases instantly (cache hit).
- Tier 2 handles 25% with real-time personalization.
- Tier 3 handles 5% with heavy reasoning.
- Average latency: <50ms. Cost: negligible.
- If any tier fails, next tier tries. If all fail, fallback works.

**What to Learn:** At scale, multi-tier isn't a luxury; it's a requirement. Design every system as a cascade. Each tier should be >2x faster than the previous.

---

### 2. Amazon — Global Compliance Screening at 2B Daily Transactions

**The Problem:** Amazon processes 2B transactions per day across 180+ countries. Each transaction must be screened for: sanctions violations, fraud, AML, export controls, child labor (in sourcing), counterfeits. Agents must run on every transaction, within latency budget.

**Architecture Decision:**

```python
# Amazon's "parallel screening" pattern

from dataclasses import dataclass
from typing import Optional

@dataclass
class ScreeningResult:
    status: str  # "approved", "review", "blocked"
    risk_score: float  # 0.0-1.0
    checks_passed: list[str]
    checks_failed: list[str]
    estimated_review_time_hours: Optional[int]

class AmazonScreeningAgent:
    """Parallel screening: do many checks at once"""
    
    async def screen_transaction(self, txn: dict, timeout_ms: int = 100) -> ScreeningResult:
        """Screen transaction before processing"""
        
        # Run all checks in parallel
        checks = await asyncio.gather(
            self._check_sanctions(txn),
            self._check_fraud(txn),
            self._check_aml(txn),
            self._check_export_controls(txn),
            self._check_counterfeits(txn),
            timeout=timeout_ms / 1000,
        )
        
        # Synthesize
        sanctions_result, fraud_result, aml_result, export_result, counterfeit_result = checks
        
        # Decision rules
        failed = [
            check for check, result in [
                ("sanctions", sanctions_result),
                ("fraud", fraud_result),
                ("aml", aml_result),
                ("export_controls", export_result),
                ("counterfeits", counterfeit_result),
            ]
            if result.failed
        ]
        
        if "sanctions" in failed or "export_controls" in failed:
            # Hard block: regulatory violation
            return ScreeningResult(
                status="blocked",
                risk_score=1.0,
                checks_passed=[c for c, _ in checks if not _.failed],
                checks_failed=failed,
                estimated_review_time_hours=None,  # Won't be reviewed
            )
        
        if "aml" in failed or "fraud" in failed:
            # Escalate for review
            return ScreeningResult(
                status="review",
                risk_score=0.7,
                checks_passed=[c for c, _ in checks if not _.failed],
                checks_failed=failed,
                estimated_review_time_hours=24,  # Manual review
            )
        
        # All pass
        return ScreeningResult(
            status="approved",
            risk_score=0.1,
            checks_passed=[c for c in ["sanctions", "fraud", "aml", "export_controls", "counterfeits"]],
            checks_failed=[],
            estimated_review_time_hours=None,
        )
    
    async def _check_sanctions(self, txn: dict) -> dict:
        """Is buyer/seller on sanctions list?"""
        
        buyer_name = txn["buyer_name"]
        seller_name = txn["seller_name"]
        
        # Check against:
        # - OFAC SDN (Office of Foreign Assets Control)
        # - EU sanctions list
        # - UN Security Council
        # - Country-specific lists
        
        buyer_sanctioned = await self.sanctions_db.lookup(buyer_name)
        seller_sanctioned = await self.sanctions_db.lookup(seller_name)
        
        failed = buyer_sanctioned or seller_sanctioned
        
        return {
            "check": "sanctions",
            "failed": failed,
            "reason": f"Buyer on list" if buyer_sanctioned else f"Seller on list" if seller_sanctioned else None,
        }
    
    async def _check_fraud(self, txn: dict) -> dict:
        """Is this transaction likely fraud?"""
        
        # ML model trained on historical fraud
        features = self._extract_fraud_features(txn)
        
        fraud_score = await self.fraud_model.predict(features)
        
        # Threshold
        failed = fraud_score > 0.8
        
        return {
            "check": "fraud",
            "failed": failed,
            "score": fraud_score,
        }
    
    async def _check_aml(self, txn: dict) -> dict:
        """Are there AML red flags?"""
        
        # Check 1: Large amount + new account?
        large_amount = txn["amount"] > 10000
        new_account = (now() - txn["account_age"]) < timedelta(days=7)
        
        if large_amount and new_account:
            return {
                "check": "aml",
                "failed": True,
                "reason": "Large amount from new account",
            }
        
        # Check 2: Rapid sequence of transactions?
        recent_txns = await self.db.count_recent_transactions(
            txn["seller_id"],
            time_window=timedelta(hours=1)
        )
        
        if recent_txns > 100:  # More than 100 txns in 1 hour
            return {
                "check": "aml",
                "failed": True,
                "reason": "Unusual transaction velocity",
            }
        
        return {
            "check": "aml",
            "failed": False,
        }
    
    async def _check_export_controls(self, txn: dict) -> dict:
        """Is seller exporting to restricted country?"""
        
        seller_country = txn["seller_country"]
        buyer_country = txn["buyer_country"]
        product_category = txn["product_category"]
        
        # EAR (Export Administration Regulations)
        # Some products can't be sold to certain countries
        
        restricted = await self.export_control_db.is_restricted(
            from_country=seller_country,
            to_country=buyer_country,
            product=product_category,
        )
        
        return {
            "check": "export_controls",
            "failed": restricted,
            "reason": f"Restricted export: {seller_country} -> {buyer_country}" if restricted else None,
        }
    
    async def _check_counterfeits(self, txn: dict) -> dict:
        """Is this likely a counterfeit product?"""
        
        # Check 1: Brand complains about seller?
        brand = txn["brand"]
        seller_id = txn["seller_id"]
        
        complaints = await self.db.count_complaints(
            brand=brand,
            seller_id=seller_id,
        )
        
        if complaints > 10:
            return {
                "check": "counterfeits",
                "failed": True,
                "reason": f"Brand {brand} has {complaints} complaints",
            }
        
        # Check 2: Price too low?
        # (Heuristic: counterfeits are often 50% below MSRP)
        product = txn["product"]
        MSRP = await self.product_db.get_msrp(product)
        seller_price = txn["price"]
        
        if seller_price < MSRP * 0.5:
            return {
                "check": "counterfeits",
                "failed": True,
                "reason": f"Price {seller_price} is 50% below MSRP {MSRP}",
            }
        
        return {
            "check": "counterfeits",
            "failed": False,
        }

# Parallel execution model
async def parallel_screening():
    """All checks run in parallel"""
    
    # Latency budget: 100ms total
    # With parallelization:
    # - sanctions: 20ms
    # - fraud: 30ms (slowest)
    # - aml: 15ms
    # - export_controls: 10ms
    # - counterfeits: 15ms
    # Total: max(20, 30, 15, 10, 15) = 30ms (well under budget)
    
    # Without parallelization: 20+30+15+10+15 = 90ms (barely fits)
    # Parallel is more resilient (if one check is slow, others finish)

# Scale implications
# 2B transactions per day
# 30ms screening per transaction
# = 2B * 30ms = 60B milliseconds = 16.7M seconds = 193 days of compute per day
# With parallelization: ~30x reduction in wall-clock time

# On 10,000 screening instances (parallel), this is:
# 60B ms / 10,000 instances = 6M ms = 1.6 hours of CPU per instance
# Very achievable
```

**Why This Works:**

- Parallel screening means all checks run simultaneously, not sequentially.
- Hard-block checks (sanctions) are checked first. If they fail, stop immediately.
- Soft-block checks (fraud) are escalated, not blocked.
- At 2B transactions per day, this saves billions in latency.

**What to Learn:** At scale, parallelization is not a nice-to-have; it's required. Every ms saved per transaction scales to millions of dollars per year.

---

### 3. DoorDash + Knowledge Graph: Hierarchical Product Search

**The Problem:** With 10M+ items, a simple keyword search returns hundreds of results. How do you surface the right item without users scrolling forever?

**Architecture Decision:**

```python
# Knowledge graph: hierarchical understanding of products

class FoodKnowledgeGraph:
    """Hierarchical product understanding"""
    
    def __init__(self):
        # Entities: restaurants, cuisines, dishes, ingredients
        # Relations: "serves", "contains", "is_popular_at", "is_seasonal"
        
        self.graph = {
            "restaurants": {},
            "cuisines": {},
            "dishes": {},
            "ingredients": {},
        }
    
    async def infer_user_intent(self, query: str) -> dict:
        """What does user REALLY want?"""
        
        # Example: "Thai green curry near me, under $20"
        
        parsed = {
            "cuisine": "Thai",
            "dish": "green curry",
            "location": "current_location",
            "price_max": 20,
            "delivery_time_max": None,
        }
        
        # Use knowledge graph to expand
        # "Thai green curry" -> restaurants that serve it
        
        candidates = await self.find_candidates(parsed)
        
        # Rank by:
        # 1. Exact match (has dish on menu)
        # 2. Nearby (distance)
        # 3. Price (under $20)
        # 4. Delivery time
        
        ranked = await self.rank_by_relevance(candidates, parsed)
        
        return {
            "intent": parsed,
            "candidates": ranked[:20],  # Top 20
        }

# In practice
# User search: "green curry"
# Without graph: 5000 results (any restaurant with "green" or "curry")
# With graph: 50 results (restaurants that specifically serve Thai green curry)

# User scroll: "I want the fancy one"
# System inference: "User wants mid-to-high end restaurant"
# Rerank: put upscale restaurants first
```

**Why This Works:**

- Knowledge graph enables semantic search (not just keyword matching).
- Hierarchical structure reduces result set from thousands to tens.
- Reranking is cheap once candidates are filtered.

**What to Learn:** At 10M+ items, a flat index is unusable. Hierarchical understanding (via knowledge graphs or taxonomies) is required.

---

### 4. Booking.com — Partner-Guest Messaging Automation

**The Problem:** Booking.com has millions of partnerships (hotels, vacation rentals). Guests message partners with questions. Partners are small businesses, often slow to respond. Agents can auto-respond to common questions. But: agents can never make commitments on behalf of partners.

**Architecture Decision:**

```python
# Booking.com's "suggested response" pattern
# Agent writes draft; partner approves before sending

class BookingMessagingAgent:
    """Compose message drafts; humans approve"""
    
    async def handle_guest_inquiry(
        self,
        inquiry: dict,
        property_id: str,
    ) -> dict:
        """Respond to guest question"""
        
        # Step 1: Classify inquiry type
        inquiry_type = await self._classify(inquiry["message"])
        
        # Step 2: Generate response draft
        if inquiry_type == "simple":
            # Simple questions: auto-respond (no human needed)
            response = await self._auto_respond(inquiry_type, inquiry)
            return {
                "status": "sent",
                "response": response,
                "human_review": False,
            }
        
        else:
            # Complex questions: suggest response (human reviews)
            suggested = await self._suggest_response(
                inquiry_type,
                inquiry,
                property_id
            )
            
            return {
                "status": "pending_review",
                "suggested_response": suggested,
                "human_review": True,
                "review_timeout_hours": 1,  # Partner must review in 1 hour
            }
    
    async def _classify(self, message: str) -> str:
        """What type of inquiry is this?"""
        
        # Simple: "What time is check-in?"
        # Simple: "Do you allow pets?"
        # Complex: "Can you negotiate the price?"
        # Complex: "I have a medical condition, what accommodations?"
        
        simple_keywords = [
            "check-in time",
            "check-out time",
            "wifi password",
            "parking",
            "pets",
            "smoking",
            "breakfast",
        ]
        
        if any(kw in message.lower() for kw in simple_keywords):
            return "simple"
        
        return "complex"
    
    async def _auto_respond(self, inquiry_type: str, inquiry: dict) -> str:
        """Respond to simple inquiries immediately"""
        
        # Template-based, not LLM
        # (Deterministic, safe)
        
        if "check-in" in inquiry["message"].lower():
            return "Check-in is at 3:00 PM. You can request early check-in here: [link]"
        
        if "pet" in inquiry["message"].lower():
            return "We welcome pets! There is a $50 pet fee. Please let us know about your pet when you arrive."
        
        # Fallback
        return "Thank you for your question. The property owner will respond soon."
    
    async def _suggest_response(
        self,
        inquiry_type: str,
        inquiry: dict,
        property_id: str,
    ) -> str:
        """Suggest response to complex inquiry"""
        
        # Gather property information
        property_info = await self.db.get_property(property_id)
        
        # Generate suggestion
        suggestion = f"""
        Thank you for your inquiry about {inquiry["subject"]}.
        
        [Agent suggestion based on property policies]
        
        Best regards,
        {property_info["name"]}
        """
        
        return suggestion
    
    async def partner_review(self, suggestion_id: str) -> dict:
        """Partner approves or edits"""
        
        # UI shows suggestion, partner can:
        # 1. Approve (send as-is)
        # 2. Edit (modify and send)
        # 3. Reject (don't send)
        
        partner_decision = await self.get_partner_decision(suggestion_id)
        
        if partner_decision["action"] == "approve":
            # Send immediately
            await self.send_message(suggestion_id, partner_decision["text"])
            return {"status": "sent"}
        
        elif partner_decision["action"] == "edit":
            # Send edited version
            edited_text = partner_decision["edited_text"]
            await self.send_message(suggestion_id, edited_text)
            return {"status": "sent"}
        
        else:
            # Reject
            return {"status": "rejected"}

# Key point
# Agent writes the draft. Partner owns the commitment.
# This satisfies: guests get fast responses, partners maintain control.
```

**Why This Works:**

- Guests get fast responses (auto-respond for simple questions).
- Partners maintain control (can edit before sending).
- Agents don't make commitments on behalf of partners.

**What to Learn:** In multi-stakeholder systems, agents should be advisors, not executors. Suggestions are fast; commitments require human approval.

---

## Key Design Question

**DoorDash runs LLMs over 10M+ products — how to make it fast AND cheap?**

My answer:

```python
class ScalableRecommendationSystem:
    """Fast + cheap at 10M items"""
    
    async def get_recommendation(
        self,
        user_id: str,
        context: dict,
        budget_ms: int = 100,
        budget_cents: float = 0.001,  # $0.00001 per request
    ) -> list[dict]:
        """Satisfy both latency and cost constraints"""
        
        # Strategy: Narrow the search space as fast as possible
        
        # Step 1: Prune to relevant restaurants (10K -> 100)
        # Criteria: cuisine, location, price, hours open
        # Cost: negligible (index lookup)
        # Latency: <5ms
        
        pruned = await self._prune_by_criteria(user_id, context)
        
        # Step 2: Rank within pruned set (100 -> 10)
        # Criteria: distance, delivery time, rating, user history
        # Cost: moderate (lightweight ML model)
        # Latency: 20-30ms
        
        ranked = await self._rank_within_pruned(pruned, user_id, context)
        
        # Step 3: Personalize within top 10 (optional)
        # Criteria: user preference, mood, occasion
        # Cost: high (expensive model)
        # Latency: expensive
        # Only run for premium users or if budget allows
        
        if budget_ms > 60 and context.get("is_premium"):
            personalized = await self._personalize_top_10(
                ranked,
                user_id,
                context,
            )
            return personalized
        
        return ranked
    
    async def _prune_by_criteria(self, user_id: str, context: dict) -> list:
        """Index lookup: very fast"""
        
        # Query: restaurant index
        # WHERE cuisine = context.cuisine
        #   AND open_at(context.time)
        #   AND price <= context.price_max
        #   AND distance(location) < 10km
        
        # This is a database index lookup (B-tree), not ML
        # Cost: $0.0001 per call
        # Latency: 3-5ms
        
        pruned = await self.restaurant_index.query(
            cuisine=context.cuisine,
            price_max=context.price_max,
            location=context.location,
            open_at=context.time,
        )
        
        return pruned  # ~100 restaurants
    
    async def _rank_within_pruned(self, pruned: list, user_id: str, context: dict) -> list:
        """Lightweight ranking model"""
        
        # Features for each restaurant:
        # 1. Distance from user
        # 2. Delivery time estimate
        # 3. Rating (avg stars)
        # 4. User has ordered from before?
        # 5. How many 5-star reviews did this user give?
        
        # Model: XGBoost (lightweight, pre-computed features)
        # Inference time: ~1ms per restaurant
        # Cost: $0.0008 per call (100 restaurants * $0.000008 per inference)
        
        scored = []
        for restaurant in pruned:
            # Fetch features (cached)
            features = await self._get_cached_features(restaurant.id)
            
            # Score (model inference)
            score = await self.ranking_model.predict(features)
            
            scored.append((restaurant, score))
        
        # Return top 10
        ranked = sorted(scored, key=lambda x: -x[1])
        return [r[0] for r in ranked[:10]]
    
    async def _personalize_top_10(self, ranked: list, user_id: str, context: dict) -> list:
        """Expensive personalization (optional)"""
        
        # Use a large model to reorder top 10
        # This is expensive (~$0.01 per call)
        # Only do it for premium users
        
        features = await self._extract_complex_features(
            ranked,
            user_id,
            context
        )
        
        reordered = await self.personalization_model.rerank(
            ranked,
            features
        )
        
        return reordered

# Economics analysis
class EconomicsAnalysis:
    def cost_breakdown(self):
        return {
            "prune": 0.0001,        # Index lookup
            "rank": 0.0008,         # Lightweight model
            "personalize": 0.01,    # Expensive model (optional)
            "total": 0.0109,        # Per call (if personalization)
        }
    
    def latency_breakdown(self):
        return {
            "prune": 5,             # ms
            "rank": 25,             # ms
            "personalize": 50,      # ms (optional)
            "total": 80,            # ms (if personalization)
        }
    
    def can_afford_personalization(self):
        # Budget: $0.001 per request
        # Personalization cost: $0.01 per request
        # NO: Can't afford for all users
        
        # Solution:
        # - Only personalize premium users (5%)
        # - Or personalize every Nth request (probabilistic)
        # - Or personalize only if user is "high value"
        
        return False

# Result
# - For 95% of users: fast (50ms) + cheap ($0.0009)
# - For 5% premium: slow (100ms) + expensive ($0.0108)
# - Global average: 52ms + $0.001 per request
# - At 10M requests/day: 5.2M ms = 1.4 hours of compute, $10K/day

# Compared to naive approach:
# - If you used big model for everyone: 500ms + $0.01 per request
# - Cost would be $100K/day (10x more expensive!)
```

---

## Cross-Domain Lessons

1. **Multi-tier is the primary architecture, not a fallback.**
   - Tier 1 (cache) handles 70%.
   - Tier 2 (lightweight ML) handles 25%.
   - Tier 3 (expensive reasoning) handles 5%.
   - This distribution means average latency is Tier 2's time, not Tier 3's.

2. **Latency compounds into revenue loss.**
   - Every 100ms slower = conversion loss.
   - At billion-user scale, this is millions per day.
   - Design for <50ms is not a luxury; it's a requirement.

3. **Parallelization saves orders of magnitude.**
   - Running 5 checks in parallel (30ms each) = 30ms total, not 150ms.
   - This is not micro-optimization; it's 5x speed improvement.

4. **Narrow the search space before applying ML.**
   - 10M items → 100K after basic pruning → 100 after filtering → 10 after ranking.
   - Cost is exponential if you use ML on 10M items.
   - Cost is linear if you prune first.

5. **Agents augment, not replace, human decision-making.**
   - Auto-respond to simple questions.
   - Suggest responses to complex questions.
   - Never make commitments on behalf of humans.

---

## Legal / Compliance: Agents That Lawyers Trust (Or Don't)

## Domain Constraints

Legal is uniquely adversarial. When an agent says "this contract is safe", a lawyer might bet their career on it. When an agent is wrong, the cost is measured in lawsuits, regulatory fines, and destroyed client relationships.

**The immutable constraints:**

- **Precision > Recall.** In legal, a false positive (saying something is a problem when it's not) is manageable. A false negative (missing a real problem) is catastrophic. Lawyers would rather review 10 false alarms than miss 1 real issue.
- **Jurisdiction-specific rules are not optional.** Contract law in California is different from New York. Immigration law in 2024 is different from 2025. Agents must know the specific rule set.
- **Explainability is non-negotiable.** Lawyers must be able to trace every legal claim back to a source. "The model said so" is professional malpractice. Citations are required.
- **Confidentiality is sacred.** Attorney-client privilege is sacred in law. A model trained on past cases exposes clients. Data must be fully anonymized or work only on client data, not shared data.

---

## Architecture Focus

The pattern across legal tech companies isn't "smarter LLMs". It's **provenance-aware design with domain expert validation**.

```
┌─────────────────────────────────────────────┐
│ Legal Document (contract, brief, motion)   │
└────────────────┬────────────────────────────┘
                 │
      ┌──────────▼──────────┐
      │ Document Parsing    │
      │ (identify sections) │
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────────────────────┐
      │ Legal Agent (narrow scope)          │
      │ "Find clauses that violate X law"   │
      │ (scope limited to single document)  │
      └──────────┬──────────────────────────┘
                 │
      ┌──────────▼──────────────────────────┐
      │ Evidence Retrieval                   │
      │ - Case law (JustiaAPI, Google Docs)  │
      │ - Statutes (state.gov, congress.gov) │
      │ - Regulations (eCFR, administrative) │
      │ - Legal restatements                 │
      └──────────┬──────────────────────────┘
                 │
      ┌──────────▼──────────────────────────┐
      │ Fact Checking                        │
      │ - Does the citation actually say...? │
      │ - Is the cite current? (not overruled?) │
      │ - Is the cite on point?              │
      └──────────┬──────────────────────────┘
                 │
      ┌──────────▼──────────────────────────┐
      │ Lawyer Review + Override             │
      │ - Lawyer can reject reasoning        │
      │ - Lawyer can dispute citations       │
      │ - Lawyer documents their decision    │
      └──────────┬──────────────────────────┘
                 │
      ┌──────────▼──────────────────────────┐
      │ Opinion Generation                   │
      │ (with full source attribution)       │
      └──────────────────────────────────────┘
```

**Key principle:** Agent finds problems. Lawyer says which problems matter. Agent never says "this is legal" without a lawyer reviewing.

---

## Case Studies: Architecture + Design Decisions

### 1. Harvey — Agent Architecture for Legal AI + Domain Expert Evaluation

**The Problem:** Building an agent that lawyers trust. Most lawyers won't trust AI with legal advice. How do you design an agent that earns trust, not just confidence?

**Architecture Decision:**

```python
# Harvey's "cite-every-claim" pattern
# Every legal claim must have a source

from dataclasses import dataclass
from typing import Optional

@dataclass
class LegalClaim:
    claim: str  # "This clause violates California contract law"
    jurisdiction: str  # "California"
    applicable_law: str  # "California Civil Code § 1670.5"
    primary_source: dict  # URL, retrieved_at, text
    supporting_sources: list[dict]  # Additional citations
    confidence: float  # 0.0-1.0
    reasoning: str  # "Because..."

class HarveyLegalAgent:
    """Agent that cites every claim"""
    
    async def analyze_contract(self, contract_text: str, jurisdiction: str) -> list[LegalClaim]:
        """Analyze contract for legal issues"""
        
        claims = []
        
        # Step 1: Identify sections (parsing, deterministic)
        sections = await self._parse_sections(contract_text)
        
        # Step 2: For each section, identify potential issues
        for section in sections:
            potential_issues = await self._identify_issues(
                section,
                jurisdiction
            )
            
            # Step 3: CRITICAL - Find sources for each issue
            for issue in potential_issues:
                sourced_claim = await self._source_claim(
                    issue,
                    jurisdiction
                )
                
                claims.append(sourced_claim)
        
        return claims
    
    async def _identify_issues(self, section: dict, jurisdiction: str) -> list[str]:
        """What might be wrong with this section?"""
        
        # Use agent to identify problems
        # Example: "This indemnification clause might be too broad"
        
        issues = []
        
        if "indemnif" in section["text"].lower():
            issues.append("Indemnification clause")
        
        if "limitation of liability" in section["text"].lower():
            issues.append("Limitation of liability")
        
        if "force majeure" in section["text"].lower():
            issues.append("Force majeure clause")
        
        return issues
    
    async def _source_claim(self, issue: str, jurisdiction: str) -> LegalClaim:
        """Find legal sources for the issue"""
        
        # Step 1: Find applicable law
        # Example: "Indemnification clauses in California are governed by..."
        
        # Search statutes
        applicable_statute = await self._find_applicable_statute(
            issue,
            jurisdiction
        )
        
        # Search case law
        supporting_cases = await self._find_relevant_cases(
            issue,
            jurisdiction
        )
        
        # Step 2: CRITICAL - Verify the source actually supports the claim
        verification = await self._verify_source(
            issue,
            applicable_statute,
            supporting_cases
        )
        
        # Construct claim
        claim = LegalClaim(
            claim=f"{issue} in {jurisdiction} may violate {applicable_statute.code}",
            jurisdiction=jurisdiction,
            applicable_law=applicable_statute.code,
            primary_source={
                "url": applicable_statute.url,
                "retrieved_at": now(),
                "text": applicable_statute.text,
            },
            supporting_sources=[
                {
                    "citation": case.citation,
                    "holding": case.holding,
                    "year": case.year,
                    "url": case.url,
                }
                for case in supporting_cases
            ],
            confidence=verification.confidence,
            reasoning=f"Under {applicable_statute.code}, {applicable_statute.summary}",
        )
        
        return claim
    
    async def _verify_source(
        self,
        issue: str,
        statute: dict,
        cases: list[dict]
    ) -> dict:
        """CRITICAL - Does the source actually support the claim?"""
        
        # This is where hallucination detection happens
        
        # Check 1: Does the statute text actually discuss this issue?
        statute_text = statute["text"]
        if issue.lower() not in statute_text.lower():
            return {
                "verified": False,
                "reason": "Statute text doesn't mention the issue",
                "confidence": 0.0,
            }
        
        # Check 2: Are the cases actually on point?
        relevant_cases = []
        for case in cases:
            # Does the case discuss the same issue?
            case_text = case["summary"]
            if issue.lower() in case_text.lower():
                relevant_cases.append(case)
        
        if not relevant_cases:
            return {
                "verified": False,
                "reason": "No cases found that discuss this issue",
                "confidence": 0.0,
            }
        
        # Check 3: Are the cases current? (Not overruled?)
        current_cases = []
        for case in relevant_cases:
            is_current = await self._check_if_overruled(case)
            if not is_current:
                continue
            current_cases.append(case)
        
        if not current_cases:
            return {
                "verified": False,
                "reason": "All relevant cases have been overruled",
                "confidence": 0.0,
            }
        
        # Check 4: What's the consensus?
        # (Single case is weaker than multiple cases agreeing)
        
        consensus_strength = len(current_cases)
        
        if consensus_strength >= 3:
            confidence = 0.9
        elif consensus_strength >= 1:
            confidence = 0.7
        else:
            confidence = 0.5
        
        return {
            "verified": True,
            "confidence": confidence,
            "reason": f"Supported by {consensus_strength} relevant cases",
        }

# Lawyer workflow
class LawyerReviewUI:
    """Lawyer reviews agent's findings"""
    
    async def review_claims(self, claims: list[LegalClaim]) -> dict:
        """Lawyer accepts or disputes claims"""
        
        # UI shows claims in order of confidence
        ranked = sorted(claims, key=lambda c: -c.confidence)
        
        for claim in ranked:
            if claim.confidence < 0.7:
                # Lawyer may want to skip low-confidence claims
                user_decision = await self.ask_lawyer(
                    "This claim is low confidence. Skip?"
                )
                if user_decision == "skip":
                    continue
            
            # Show claim with sources
            print(f"\n{claim.claim}")
            print(f"Applicable Law: {claim.applicable_law}")
            print(f"Statute URL: {claim.primary_source['url']}")
            print(f"Confidence: {claim.confidence:.0%}")
            print(f"\nSupporting Cases:")
            for case in claim.supporting_sources:
                print(f"  - {case['citation']} ({case['year']}): {case['holding']}")
            
            # Lawyer decision
            decision = await self.ask_lawyer(
                "Agree with this finding? [yes/no/dispute]"
            )
            
            if decision == "dispute":
                # Lawyer provides their reasoning
                lawyer_reasoning = await self.ask_lawyer(
                    "Why do you dispute this?"
                )
                
                # Log for model training
                await self.log_lawyer_dispute({
                    "claim": claim,
                    "lawyer_dispute_reason": lawyer_reasoning,
                })

# Model improvement
class ContinuousImprovement:
    """Learn from lawyer feedback"""
    
    async def train_on_lawyer_disputes(self):
        """Improve based on what lawyers disagreed with"""
        
        # Collect disputes
        disputes = await self.db.get_lawyer_disputes()
        
        # Pattern: "Agent said X but lawyer disagreed because..."
        
        for dispute in disputes:
            # What was the agent wrong about?
            claim = dispute["claim"]
            lawyer_reason = dispute["lawyer_dispute_reason"]
            
            # Example:
            # Claim: "Indemnity clause violates CA law"
            # Lawyer: "Actually, it's enforceable because of CA Civil Code § 2782"
            
            # Training signal: This specific claim + law combination
            # results in a false positive
            
            # Tag these patterns and improve
```

**Why This Works:**

- Every claim is cited. If the source doesn't support the claim, the lawyer catches it.
- Confidence scores are based on evidence (number of supporting cases), not just model certainty.
- Lawyer feedback is systematically collected for improvement.

**What to Learn:** In legal, citability is the feature. Agents without citations are not useful; they're dangerous.

---

### 2. Thomson Reuters — Multi-Domain Legal/Tax/Compliance Orchestration

**The Problem:** Legal issues cross domains. A contract might have tax implications. A tax filing might have compliance implications. Agents need to understand multi-domain interactions.

**Architecture Decision:**

```python
# Thomson Reuters' "domain-specific agents + orchestrator" pattern

class LegalDomain:
    """Agent specialized in contracts"""
    pass

class TaxDomain:
    """Agent specialized in tax code"""
    pass

class ComplianceDomain:
    """Agent specialized in regulatory requirements"""
    pass

class MultiDomainOrchestrator:
    """Route to right domain(s)"""
    
    def __init__(self):
        self.legal_agent = LegalDomain()
        self.tax_agent = TaxDomain()
        self.compliance_agent = ComplianceDomain()
    
    async def analyze_contract(self, contract: str) -> dict:
        """Analyze contract across domains"""
        
        # Step 1: Legal analysis
        legal_findings = await self.legal_agent.analyze(contract)
        
        # Step 2: Check if legal findings have tax implications
        tax_implications = []
        for finding in legal_findings:
            if self._has_tax_implications(finding):
                # Escalate to tax agent
                tax_finding = await self.tax_agent.analyze(
                    contract,
                    legal_context=finding
                )
                tax_implications.append(tax_finding)
        
        # Step 3: Check if there are compliance implications
        compliance_implications = []
        for finding in legal_findings + tax_implications:
            if self._has_compliance_implications(finding):
                compliance_finding = await self.compliance_agent.analyze(
                    contract,
                    prior_findings=[finding]
                )
                compliance_implications.append(compliance_finding)
        
        # Step 4: Synthesize
        return {
            "legal": legal_findings,
            "tax": tax_implications,
            "compliance": compliance_implications,
            "synthesis": await self._synthesize(
                legal_findings,
                tax_implications,
                compliance_implications,
            ),
        }
    
    def _has_tax_implications(self, legal_finding: dict) -> bool:
        """Does this legal issue affect taxes?"""
        
        tax_keywords = [
            "payment", "revenue", "deduction", "cost", "basis",
            "capital gains", "ordinary income", "partnership",
        ]
        
        if any(kw in legal_finding["claim"].lower() for kw in tax_keywords):
            return True
        
        return False
    
    def _has_compliance_implications(self, finding: dict) -> bool:
        """Does this issue affect compliance?"""
        
        compliance_keywords = [
            "export", "sanctions", "GDPR", "CCPA", "HIPAA",
            "AML", "KYC", "regulatory", "approval",
        ]
        
        if any(kw in finding["claim"].lower() for kw in compliance_keywords):
            return True
        
        return False
    
    async def _synthesize(
        self,
        legal: list,
        tax: list,
        compliance: list
    ) -> str:
        """Synthesize findings across domains"""
        
        # Example synthesis:
        # "This payment term is legally enforceable but has tax
        #  implications (capital gains treatment). Also check
        #  HIPAA compliance if client data is involved."
        
        synthesis = "Based on analysis across legal, tax, and compliance:\n\n"
        
        if legal:
            synthesis += f"LEGAL: {len(legal)} findings\n"
            for finding in legal:
                synthesis += f"  - {finding['claim']}\n"
        
        if tax:
            synthesis += f"\nTAX: {len(tax)} implications\n"
            for finding in tax:
                synthesis += f"  - {finding['claim']}\n"
        
        if compliance:
            synthesis += f"\nCOMPLIANCE: {len(compliance)} implications\n"
            for finding in compliance:
                synthesis += f"  - {finding['claim']}\n"
        
        synthesis += "\nACTION: Lawyer review recommended"
        
        return synthesis
```

**Why This Works:**

- Each domain has a specialized agent (not one monolithic LLM).
- Orchestrator routes based on content, not user preference.
- Cross-domain implications are caught by escalation.

**What to Learn:** In complex domains (legal, tax, compliance), specialize by domain. Let domain experts build domain agents. Orchestrate at a higher level.

---

### 3. Navismart AI — Immigration Document Automation

**The Problem:** Immigration law is jurisdiction-specific and changes constantly. An agent must know: which country's rules? What's the current filing deadline? What documents are required?

**Architecture Decision:**

```python
# Navismart's "jurisdiction-aware + real-time update" pattern

from dataclasses import dataclass
from datetime import datetime

@dataclass
class ImmigrationContext:
    from_country: str
    to_country: str
    visa_type: str  # "H-1B", "Green Card", etc.
    current_date: datetime
    applicant_info: dict  # Age, education, work history, etc.

class ImmigrationAgent:
    """Agent specialized in immigration law"""
    
    def __init__(self):
        # Load jurisdiction-specific rules
        self.rules_by_jurisdiction = {}
        self._load_all_jurisdictions()
        
        # Set up real-time updates
        self._subscribe_to_policy_changes()
    
    def _load_all_jurisdictions(self):
        """Load rules for all immigration jurisdictions"""
        
        # Example: US H-1B
        self.rules_by_jurisdiction["US_H1B"] = {
            "filing_deadline": {
                "2024": datetime(2024, 4, 1),
                "2025": datetime(2025, 3, 17),  # Announced in advance
            },
            "required_documents": [
                "Form I-129",
                "Labor Condition Application (LCA)",
                "Job description",
                "Proof of degree",
                "Passport",
            ],
            "processing_time": 180,  # days
            "approval_rate": 0.70,  # 70% historically
        }
        
        # Example: Canada Express Entry
        self.rules_by_jurisdiction["CA_EE"] = {
            "crs_score_required": 460,  # Current cutoff
            "processing_time": 180,
            "required_documents": [
                "ECA (Educational Credential Assessment)",
                "Language test scores (IELTS or TEF)",
                "Passport",
                "Medical exam",
                "Police clearance",
            ],
        }
    
    def _subscribe_to_policy_changes(self):
        """Monitor policy changes in real-time"""
        
        # Subscribe to USCIS alerts
        # Subscribe to Canada Immigration alerts
        # Subscribe to UK Home Office updates
        
        # When policy changes, update rules
        async def on_policy_change(country, change):
            self.rules_by_jurisdiction[country].update(change)
            
            # Log for audit
            await self.log_policy_change(country, change)
    
    async def generate_checklist(
        self,
        context: ImmigrationContext
    ) -> dict:
        """Generate document checklist for applicant"""
        
        # Step 1: Identify applicable rules
        jurisdiction_key = f"{context.to_country}_{context.visa_type}"
        rules = self.rules_by_jurisdiction.get(jurisdiction_key)
        
        if not rules:
            return {
                "error": f"No rules found for {context.to_country} {context.visa_type}",
                "action": "Manual review required",
            }
        
        # Step 2: Check if deadline has passed
        current_filing_deadline = rules.get("filing_deadline", {}).get(
            str(context.current_date.year)
        )
        
        if context.current_date > current_filing_deadline:
            return {
                "error": "Filing deadline has passed",
                "next_deadline": rules.get("filing_deadline", {}).get(
                    str(context.current_date.year + 1)
                ),
                "action": "Deadline is closed; wait for next year",
            }
        
        # Step 3: Check applicant eligibility
        eligibility = await self._check_eligibility(context, rules)
        
        if not eligibility["eligible"]:
            return {
                "error": eligibility["reason"],
                "action": eligibility["recommendation"],
            }
        
        # Step 4: Generate checklist
        checklist = {
            "visa_type": context.visa_type,
            "filing_deadline": current_filing_deadline,
            "processing_time": f"{rules['processing_time']} days",
            "documents": [
                {
                    "document": doc,
                    "required": True,
                    "processing_notes": await self._get_processing_notes(
                        doc,
                        context
                    ),
                }
                for doc in rules["required_documents"]
            ],
            "success_rate": rules.get("approval_rate", "Unknown"),
            "notes": [
                "Submit all documents at once",
                "Ensure documents are certified/notarized if required",
                f"Processing time: approximately {rules['processing_time']} days",
            ],
        }
        
        return checklist
    
    async def _check_eligibility(
        self,
        context: ImmigrationContext,
        rules: dict
    ) -> dict:
        """Is applicant eligible?"""
        
        # Rule-based checks (jurisdiction-specific)
        
        # H-1B specific: Must have bachelor's degree
        if context.visa_type == "H-1B":
            if context.applicant_info.get("degree_level") != "bachelor":
                return {
                    "eligible": False,
                    "reason": "H-1B requires bachelor's degree or equivalent",
                    "recommendation": "Consider other visa categories",
                }
        
        # Express Entry specific: CRS score
        if context.visa_type == "EE":
            crs_required = rules.get("crs_score_required")
            crs_actual = await self._calculate_crs_score(context.applicant_info)
            
            if crs_actual < crs_required:
                return {
                    "eligible": False,
                    "reason": f"CRS score {crs_actual} < required {crs_required}",
                    "recommendation": f"Improve score by {crs_required - crs_actual} points",
                }
        
        return {"eligible": True}

# Key insight
# - Rules are VERSIONED by year/jurisdiction
# - Updates are pushed in real-time
# - Eligibility checks are deterministic (not ML-based)
# - Lawyer still reviews before applicant submits
```

**Why This Works:**

- Jurisdiction rules are explicitly versioned and updated.
- Checklists are generated from rules, not hallucinated.
- Eligibility checks are rule-based, not heuristic-based.

**What to Learn:** In legal domains with frequent policy changes, build systems that are updatable without retraining. Treat rules as data, not knowledge baked into the model.

---

### 4. Activeloop — Memory Agents for Patent Processing

**The Problem:** Patent prosecution involves 1000+ pages of documents: specifications, claims, office actions, prior art, response briefs. Agents need to keep track of what's been discussed, what's been rejected, what the current status is.

**Architecture Decision:**

```python
# Activeloop's "persistent memory for legal documents" pattern

class PatentProcessingMemory:
    """Memory system for patent prosecution"""
    
    def __init__(self, patent_id: str):
        self.patent_id = patent_id
        self.memory_store = DeepLake(
            name=f"patent_memory_{patent_id}",
            read_only=False,
        )
    
    async def ingest_office_action(self, office_action_text: str):
        """When USPTO issues an office action, ingest it into memory"""
        
        # Parse office action
        rejections = await self._parse_rejections(office_action_text)
        
        # Store in memory
        memory_entry = {
            "document_type": "office_action",
            "date": now(),
            "rejections": rejections,
            "deadline": self._calculate_deadline(office_action_text),
        }
        
        await self.memory_store.add(memory_entry)
    
    async def remember_prior_art(self, reference: str):
        """Store references we've cited"""
        
        memory_entry = {
            "document_type": "prior_art",
            "reference": reference,
            "cited_by_examiner": False,  # True if examiner brought it up
        }
        
        await self.memory_store.add(memory_entry)
    
    async def current_status(self) -> str:
        """What's the current state?"""
        
        # Query memory: What rejections are outstanding?
        outstanding = await self.memory_store.search(
            query="outstanding rejections",
            limit=10,
        )
        
        if not outstanding:
            return "All rejections have been addressed"
        
        status = "Outstanding Rejections:\n"
        for rejection in outstanding:
            status += f"  - {rejection['rejection']}\n"
        
        return status
    
    async def draft_response(self) -> str:
        """Draft a response to office action"""
        
        # Retrieve context from memory
        context = await self.memory_store.search(
            query="previous arguments for this claim",
            limit=5,
        )
        
        # Generate response
        response = await self._generate_response(context)
        
        # Store in memory for future reference
        await self.memory_store.add({
            "document_type": "response",
            "arguments": response,
            "date": now(),
        })
        
        return response

# Why this matters
# Patent prosecution can last 5-10 years, with 50+ office actions
# Without memory, agent would repeat arguments, contradict itself
# With memory, agent maintains consistency across years

# Example interaction
# Year 1: "Claim is novel because it uses technique X"
# Year 3: Examiner: "Prior art Y anticipates claim"
# Without memory: "But we said X was novel!" (confusion)
# With memory: "We previously argued X. Prior art Y doesn't show X. Here's proof."
```

**Why This Works:**

- Memory persists across years of prosecution.
- Agent can reference what was said before, what was rejected, what was accepted.
- This enables coherent, consistent prosecution strategy.

**What to Learn:** Legal work is inherently stateful. Agents need memory systems that can be searched, updated, and referenced. Don't treat legal documents as one-off analysis; treat them as a corpus that builds over time.

---

## Key Design Question

**When an agent says "this clause violates local law" — what architecture gives you confidence that statement is trustworthy?**

My answer:

```python
class TrustworthyLegalAgent:
    """Agent that earns lawyer trust"""
    
    async def analyze_clause(
        self,
        clause_text: str,
        jurisdiction: str,
    ) -> dict:
        """Analyze clause with full provenance"""
        
        # Phase 1: IDENTIFY the issue
        potential_issues = await self._identify_issues(
            clause_text,
            jurisdiction
        )
        
        # Phase 2: RESEARCH the law
        legal_findings = []
        for issue in potential_issues:
            # Find primary sources
            statute = await self._find_statute(issue, jurisdiction)
            cases = await self._find_cases(issue, jurisdiction)
            
            legal_findings.append({
                "issue": issue,
                "statute": statute,
                "cases": cases,
            })
        
        # Phase 3: VERIFY each source
        verified = []
        for finding in legal_findings:
            # Does the statute actually prohibit this?
            statute_applies = await self._verify_statute(
                finding["statute"],
                finding["issue"],
                clause_text
            )
            
            if not statute_applies:
                continue
            
            # Are the cases current?
            current_cases = await self._filter_current_cases(
                finding["cases"]
            )
            
            if not current_cases:
                continue
            
            verified.append({
                "issue": finding["issue"],
                "statute": finding["statute"],
                "cases": current_cases,
                "confidence": self._calculate_confidence(
                    statute_ok=statute_applies,
                    cases=current_cases
                ),
            })
        
        # Phase 4: PRESENT with full attribution
        analysis = {
            "clause_text": clause_text,
            "jurisdiction": jurisdiction,
            "findings": verified,
            "summary": await self._synthesize(verified),
            "disclaimer": "This is legal research, not legal advice. Consult a lawyer.",
            "timestamp": now(),
            "model_version": "2.1.0",
        }
        
        # Phase 5: ALLOW LAWYER TO VERIFY
        # Lawyer sees: clause, analysis, every source cited
        # Lawyer can: accept, dispute, edit
        
        return analysis
    
    async def _verify_statute(
        self,
        statute: dict,
        issue: str,
        clause_text: str
    ) -> bool:
        """Does the statute actually apply here?"""
        
        # CRITICAL: Read the statute text
        statute_text = statute["text"]
        
        # Check 1: Does statute mention the issue?
        if issue.lower() not in statute_text.lower():
            return False
        
        # Check 2: Is the statute currently in force?
        if statute.get("repealed"):
            return False
        
        # Check 3: Does the clause text trigger the statute?
        # Example: statute says "no unilateral termination"
        # Clause says "Party A may terminate at will"
        # These clearly conflict
        
        conflict = await self._detect_conflict(
            statute_text,
            clause_text
        )
        
        return conflict
    
    async def _calculate_confidence(
        self,
        statute_ok: bool,
        cases: list
    ) -> float:
        """How confident should we be?"""
        
        if not statute_ok:
            return 0.0
        
        # Confidence based on case law consensus
        if len(cases) >= 3:
            return 0.95  # Multiple courts agree
        elif len(cases) == 1:
            return 0.70  # Single case
        else:
            return 0.50  # Statute only, no cases
    
    async def _synthesize(self, verified: list) -> str:
        """Human-readable summary"""
        
        if not verified:
            return "No legal violations found based on current research."
        
        summary = f"Found {len(verified)} potential issues:\n\n"
        
        for finding in verified:
            summary += f"ISSUE: {finding['issue']}\n"
            summary += f"STATUTE: {finding['statute']['citation']}\n"
            summary += f"CASE LAW: {len(finding['cases'])} relevant cases\n"
            summary += f"CONFIDENCE: {finding['confidence']:.0%}\n"
            summary += f"RECOMMENDATION: Consult a lawyer in {finding['statute']['jurisdiction']}\n\n"
        
        return summary

# The answer: Trust comes from:
# 1. Every claim has a source (statute or case)
# 2. Every source is verified (text actually says X)
# 3. Every source is current (not overruled, not repealed)
# 4. Confidence is based on evidence, not model certainty
# 5. Lawyer can see full chain of reasoning
# 6. Lawyer can dispute any step
# 7. System learns from disputes
```

---

## Cross-Domain Lessons

1. **Citations are the foundation of trustworthiness.**
   - In legal, "because the model said so" is worthless.
   - Every claim must trace back to statute, case law, or regulation.
   - If the source doesn't actually support the claim, the system fails.

2. **Jurisdiction matters more than generality.**
   - Don't build one legal agent. Build jurisdiction-specific agents.
   - Law in California ≠ law in New York ≠ law in Germany.
   - Agents must know the specific rule set.

3. **Precision > Recall in high-stakes domains.**
   - A false positive (flag a non-issue) is forgivable.
   - A false negative (miss a real issue) is catastrophic.
   - Design accordingly.

4. **Legal work is stateful.**
   - Contracts, prosecutions, litigations all evolve over time.
   - Agents need memory systems to track changes.
   - Context from prior interactions is essential.

5. **Lawyer review is not a fallback; it's the primary interface.**
   - Agents provide analysis. Lawyers make decisions.
   - The agent's job is to reduce lawyer cognitive load, not replace lawyer judgment.
   - If you remove the lawyer from the loop, you've built a dangerous product.

6. **Policy changes are continuous.**
   - Immigration rules change yearly. Tax codes change monthly.
   - Systems must be updatable without retraining.
   - Build rules as data, not knowledge baked into the model.

---

## HR & Recruiting: Domain Deep Dive

When you're hiring someone, you're making a decision that shapes their entire career trajectory. That's why HR is genuinely different from other domains. You can't A/B test your way out of discriminatory outcomes. You can't iterate with users who've already been rejected. And you can't explain away unfairness as "the model is just following the data."

This is where agentic systems hit their hardest constraint: **human judgment at scale**. The agents aren't smart enough to replace it. They're smart enough to *amplify* biases if you're not careful.

## Domain Constraints That Actually Matter

### 1. **Employment Law Is Everywhere**
Different jurisdictions have completely different rules:
- US: Title VII (disparate impact), ADEA (age discrimination), ADA (disability accommodations)
- EU: GDPR (data retention), directive against discrimination (much stricter than US)
- UK: Equality Act 2010 + retained EU law tensions
- Canada: CHRC human rights focus

An agent trained on US hiring data firing wrongly on UK data isn't a problem—it's a lawsuit waiting to happen.

### 2. **Bias Isn't Just in the Training Data**
You can have clean training data and still build a biased system:
- **Proxy bias**: using school ranking (correlates with wealth) instead of ability
- **Feedback loop bias**: rejected candidates who would have succeeded were never hired, so the model never learns
- **Aggregation bias**: what works on average for one demographic fails catastrophically for a minority subgroup
- **Deployment bias**: the agent gets worse as recruiting patterns change (hiring freezes, rapid growth)

### 3. **Candidate Experience Is Asymmetric**
A recruiter rejecting you is one conversation. An automated system rejecting you *without explanation* is gaslighting at scale. Candidates have no way to appeal. They don't know why they were screened out.

### 4. **Data Privacy Kills Utility**
GDPR says you can't store CV data for 2 years waiting for the next role. Most recruiting systems *need* that history to catch patterns. Result: European recruiting agents work with less signal than US ones.

### 5. **Evaluation Metrics Don't Capture Fairness**
Accuracy ≠ fairness. You can build a system that's 95% accurate at predicting hire success but 40% biased against women in technical roles because the feedback loop only cares about "hired people who succeeded," not "people who would have succeeded if hired."

---

## Architecture Focus: The LinkedIn Four-Agent System

LinkedIn handles millions of recruiting interactions yearly. Their production approach gives us a roadmap: **isolation + staged gates + explainability at every step**.

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECRUIT INTENT DETECTION                      │
│  (Intent: "Find backend engineers in NYC who know Rust")         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
       ┌───────────────┴────────────────┐
       │                                 │
   ┌───▼─────────┐           ┌──────────▼────────┐
   │  QUERY      │           │  CANDIDATE SEARCH │
   │  REFINEMENT │           │  & RANKING AGENT  │
   │  AGENT      │           │                   │
   │             │           │  - Source control │
   │  Why:       │           │  - Skill matching │
   │  Raw input  │           │  - Locality filter│
   │  is noisy   │           │  - Bias detection │
   └────┬────────┘           └──────────┬────────┘
        │                                │
        └────────────────┬───────────────┘
                         │
              ┌──────────▼──────────┐
              │   FIT ASSESSMENT    │
              │   AGENT             │
              │                     │
              │  - Role alignment   │
              │  - Trajectory check │
              │  - Explainability   │
              │  - Fairness audit   │
              └──────────┬──────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────▼────┐                   ┌─────▼──────┐
    │ HUMAN   │                   │ HUMAN      │
    │ RECRUITER                   │ DECISION   │
    │ LOOP    │                   │ REQUIRED   │
    │         │                   │ (Final)    │
    └─────────┘                   └────────────┘
```

### **Agent 1: Query Refinement Agent**
**Why this exists**: Raw recruiting requests are biased garbage.
- "I want people just like our current team" → all white men
- "I want growth mindset" → unmeasurable proxy for something else
- "I want someone who can hit the ground running" → discriminates against candidates needing accommodations

**What it does**:
- Rewrites vague queries into measurable criteria
- Flags problematic language automatically
- Suggests inclusive alternatives ("experienced" vs. "5+ years" — the latter is measurable)

```python
class QueryRefinement(Agent):
    def assess_bias_signals(self, query: str) -> BiasReport:
        """
        Red flags:
        - Cultural fit language (discriminatory proxy)
        - Vague personality traits
        - Age/experience conflation
        - Overspecification (too many "must-haves")
        """
        bias_signals = self.extractor.extract(
            query,
            patterns=[
                "culture fit",
                "team player",
                "native-like fluency",  # English fluency for non-English roles
                "young energy",
                "recent grad",
            ]
        )
        
        if bias_signals:
            return BiasReport(
                issues=bias_signals,
                suggested_fixes=self.suggest_alternatives(bias_signals),
                recommend_human_review=True
            )
        
        return self.refine_to_measurable_criteria(query)
```

**Key decision**: This agent *always* flags ambiguous queries for human review. The cost of false positives (delaying a hiring request) is tiny vs. the cost of false negatives (systematically excluding a protected class).

### **Agent 2: Candidate Search & Ranking Agent**
**Why this exists**: Not all ranking is equal. Relevance ≠ fairness.

**What it does**:
- Searches candidates using refined criteria
- Ranks by fit
- **Maintains fairness metrics in parallel**: How are different demographic groups distributed in the top-50?

```python
class CandidateRankingAgent(Agent):
    def rank_candidates(
        self,
        query: RefinedQuery,
        candidates: List[Profile]
    ) -> RankedList:
        """
        Multi-objective ranking:
        1. Skill relevance (primary)
        2. Fairness metrics (secondary constraint)
        
        NOT: "Filter by fairness then rank by skill"
        YES: "Rank by skill, audit fairness, report disparate impact"
        """
        
        ranked = self.rank_by_relevance(candidates, query)
        
        # Audit: What's the demographic distribution?
        fairness_audit = self.audit_disparate_impact(
            ranked[:50],
            baseline_distribution=self.get_eligible_pool_distribution()
        )
        
        if fairness_audit.estimated_disparate_impact > 0.80:
            # 4/5ths rule: selection rate of protected group < 80%
            return RankedListWithWarning(
                results=ranked,
                warning=f"Estimated disparate impact: {fairness_audit}",
                recommend_human_review=True
            )
        
        return ranked
```

**Key decision**: Fairness metrics are *alongside* ranking, not replacing it. You don't pre-filter candidates. You rank fairly, measure impact, *then* ask humans.

### **Agent 3: Fit Assessment Agent**
**Why this exists**: A candidate might match the job description but be overqualified, underqualified, or a flight risk.

**What it does**:
- Analyzes career trajectory (does it show relevant growth?)
- Identifies role alignment gaps
- Generates explanations for every assessment

```python
class FitAssessmentAgent(Agent):
    def assess_trajectory(
        self,
        candidate: Profile,
        role: Role
    ) -> FitAssessment:
        """
        Key insight: Trajectory matters more than current state.
        
        Someone who was a barista → bootcamp → junior dev → mid dev
        is higher-signal for growth than someone with degree+experience
        """
        
        trajectory = self.parse_career_path(candidate.experience)
        
        assessment = FitAssessment(
            role_alignment=self.assess_skills(candidate, role),
            trajectory_fit=self.assess_growth_pattern(trajectory, role),
            flight_risk=self.estimate_retention(
                candidate,
                role,
                exclude=["salary"]  # fairness: don't assume retention by demo
            ),
            explanations=[
                f"Trajectory shows {trajectory.growth_rate:.1%} skill increase per year",
                f"Current skills match {assessment.role_alignment:.0%} of job description",
                f"Estimated tenure: {assessment.flight_risk.years} years"
            ]
        )
        
        return assessment
```

**Key decision**: Generate explanations for *every candidate*, not just rejections. If you hire someone, the hiring manager sees "Why we think you'll succeed here." If you don't, the candidate (if they ask via appeals process) sees "We assessed your trajectory relative to role growth and found...". This makes the system auditable.

### **Agent 4: Decision Support Agent**
**Why this exists**: This is where humans stay in control.

**What it does**:
- Summarizes all prior agent assessments
- Flags conflicts (query agent says "good" but fit agent says "trajectory mismatch")
- Recommends next steps
- Logs decision rationale for every hire/reject

```python
class DecisionSupportAgent(Agent):
    def prepare_hiring_decision(
        self,
        candidate: Profile,
        query_refined: RefinedQuery,
        ranking: RankingResult,
        fit: FitAssessment
    ) -> HiringDecision:
        """
        This agent NEVER makes the final call.
        It prepares everything a human recruiter needs to decide.
        """
        
        # Detect conflicts
        conflicts = self.detect_conflicts(query_refined, fit, ranking)
        
        # Prepare summary
        summary = HiringDecision(
            candidate=candidate,
            recommendation="ADVANCE TO NEXT ROUND",
            confidence=0.87,
            
            reasoning=[
                f"Query match: {ranking.percentile:.0%}",
                f"Trajectory fit: {fit.trajectory_fit:.0%}",
                f"Fairness impact: No disparate impact detected",
            ],
            
            conflicts=conflicts,
            flags=[
                "Underrepresented demographic group (women in engineering)",
                "Recent pivot from adjacent domain"
            ],
            
            human_decision_checkpoints=[
                "Does trajectory growth pattern match your standards?",
                "Are you comfortable with domain transition?",
            ]
        )
        
        return summary
```

**Key decision**: The agent prepares, humans decide. The system logs *why* humans decided, so you can audit against discrimination later.

---

## Case Studies: Where the Theory Breaks Down

### **Case Study 1: LinkedIn's Hiring Assistant Platform**

**The Problem**
LinkedIn built a hiring assistant that helped recruiters screen candidates faster. Initial version: 95% accuracy at predicting "will be hired."

Six months in, diversity metrics showed: 40% fewer women in the "recommended" tier vs. the overall pool.

**What Happened**
The training data was clean. No obvious bias there. But the feedback loop was poisoned:
- Model trained on "people who were hired"
- But data on "people who would have succeeded if hired" didn't exist
- Result: Model learned "we hire people like the ones we've already hired"
- And hiring had been demographically skewed

**The Architecture Fix**
```
BEFORE:
Candidates → Model → Ranking → Recruiter Reviews → DECISION

AFTER:
Candidates → Model → Ranking ┐
                              ├→ Fairness Audit (background) → Combined view → Recruiter
            ↓                 │
      Fairness check ──────────┘
      (demographic distribution
       of top-N)
```

They added a background fairness audit that ran in parallel to ranking. Recruiters saw both the ranking and a fairness report ("Your top 20 is 25% women. The applicant pool is 35% women. Consider expanding your review set.").

**Key Numbers**
- Eliminated gender disparate impact within 3 months
- Hiring latency increased 2 hours per candidate (fairness review time)
- Diversity of hired cohorts increased 18% in first year
- Zero legal challenges (explainability helped)

**Design Decision: Why Parallel, Not Sequential?**
If you filter candidates by fairness first, then rank, you're doing affirmative action. If you rank first, then filter for fairness, you're doing bias mitigation. The legal distinction matters.

LinkedIn chose: Rank by pure skill → Audit for fairness → Ask humans to decide how much to care.

---

### **Case Study 2: Rippling's Enterprise HR Agent**

**The Problem**
Rippling manages HR, IT, and finance for enterprises. They needed agents to:
1. Process hiring requests from managers
2. Create Okta/JIRA/Slack accounts automatically
3. Assign equipment
4. Schedule onboarding

But they needed to do this *without* allowing agents to accidentally violate employment law (e.g., an agent could infer disability from a reasonable accommodation request and pre-filter them out of future hiring).

**The Architecture**
```
Manager Request:
"I need 5 backend engineers"
        │
        ▼
┌────────────────────────────────────────┐
│  INTENT CLASSIFIER                     │
│  Is this: hiring / transfer / role     │
│  change / equipment / accommodation?   │
└─────────┬──────────────────────────────┘
          │
          ├─→ HIRING → Query Refinement Agent
          │
          ├─→ TRANSFER → Role Availability Agent
          │
          ├─→ ACCOMMODATION → [HARD STOP]
          │    Human Compliance Team ONLY
          │    (No agent touches disability data)
          │
          └─→ EQUIPMENT → Auto-fulfillment Agent

         ┌──────────────────────────────────┐
         │    ISOLATED DATA COMPARTMENTS    │
         │                                  │
         │  - Hiring data (searchable)      │
         │  - Medical/disability data       │
         │    (locked, compliance only)     │
         │  - Compensation (masked)         │
         │  - Termination (locked)          │
         └──────────────────────────────────┘
```

**Key Design: Data Isolation**
Rippling's agents can *never* see protected class data (disability, medical, age if not relevant to role). If a system needs that data, it's not an agent—it's a human workflow with audit logging.

```python
class ProtectedDataPolicy:
    """
    Some data is too dangerous for agents to touch.
    Even if the agent would use it "fairly," the risk of leakage is too high.
    """
    
    AGENT_ACCESSIBLE = {
        "skills", "experience", "education",
        "job_title", "department"
    }
    
    HUMAN_ONLY = {
        "age", "disability", "medical_history",
        "immigration_status", "religion", "sexual_orientation",
        "compensation_history", "termination_reasons"
    }
    
    def create_agent_candidate_record(
        self,
        candidate: FullCandidate
    ) -> AgentAccessibleRecord:
        """
        Strip sensitive fields. If agent needs one of them,
        the system raises an exception.
        """
        return AgentAccessibleRecord(
            **{k: v for k, v in candidate.items()
               if k in self.AGENT_ACCESSIBLE}
        )
```

**Key Numbers**
- 40,000+ onboarding flows automated per year
- Zero discrimination claims related to automation
- Compliance audit time cut by 60% (because audit trail was designed in from day one)

**Design Decision: Why Not Train Agents on All Data with Fairness Constraints?**
Because fairness constraints are software. They can be bypassed. Discrimination cases hinge on *intent*: if an agent had access to protected class data, juries assume it used it, intent or not. Better to architecturally prevent access than to rely on software constraints.

---

### **Case Study 3: The Hiring Assistant That Filtered for "Culture Fit" (And Got Sued)**

**The Problem**
A major tech company deployed an internal agent to screen resumes. It was trained on resumes of current employees and whether they were "successful" (still employed, promoted, or high-performing).

The agent learned to downrank candidates who:
- Went to state schools (vs. elite schools represented in the successful cohort)
- Had non-English job titles on resume
- Had unexplained employment gaps
- Switched jobs frequently

All correlated with protected classes: first-gen college attendees, immigrants, women (more likely to have gaps), people with disabilities.

The company used the agent for 8 months. Diversity metrics tanked.

**What Happened**
A candidate was rejected. Her background: immigrant, state school, two employment gaps (one for childcare, not disclosed). She sued for disparate impact.

The company's legal team realized: The agent *couldn't explain why* it rejected her. "The model said so" isn't a legal defense.

**The Architecture Lessons**
1. **Explainability isn't optional for high-stakes decisions**
   - Candidates must be able to understand why they were rejected
   - Companies must be able to defend decisions in court
   - Opaque models fail both tests

2. **"Success" as a training target is circular**
   - You trained on "people we hired who worked out"
   - So the model learns "hire people like the ones we hired"
   - You've architecturally guaranteed perpetuating historical bias

3. **Feedback loops must include negative examples**
   - Include candidates you *didn't* hire who would have succeeded
   - Include candidates you *did* hire who didn't succeed
   - This breaks the selection bias

**The Fix**
They rebuilt using:
- Structured job descriptions (measurable criteria, not vibes)
- Explicit training data: "Why we hired person X" + "Why person Y would have succeeded if hired"
- Candidate-facing explanations: "We assessed your resume against 7 role criteria. You matched 5. Here's why we didn't advance you."
- Annual bias audits by third-party firm

---

### **Case Study 4: Bias Detection as an Architectural Component**

**The Pattern**
The best recruiting systems don't try to be fair. They actively *detect* bias.

```python
class RecruitingFairnessAudit(Agent):
    """
    Run in background, independent of main ranking pipeline.
    Purpose: Surface disparate impact before it happens.
    """
    
    def audit_decision_outcomes(
        self,
        decisions: List[HiringDecision],
        period: str = "weekly"
    ) -> FairnessReport:
        """
        The 4/5ths rule:
        If selection rate of protected group is < 80% of majority group,
        you have evidence of disparate impact.
        """
        
        by_demographic = self.group_by_protected_class(decisions)
        
        for protected_class, group_decisions in by_demographic.items():
            selection_rate = group_decisions.acceptance_rate
            baseline = by_demographic["majority"].acceptance_rate
            
            impact_ratio = selection_rate / baseline
            
            if impact_ratio < 0.80:
                alert = DisprateImpactAlert(
                    affected_class=protected_class,
                    impact_ratio=impact_ratio,
                    affected_count=len(group_decisions),
                    recommendation="Human review required before proceeding"
                )
                self.alert_compliance(alert)
        
        return FairnessReport(outcomes=outcomes)
```

**Key Insight**
Every recruiting system should have a background process that audits for disparate impact. This isn't "preventing bias"—bias is already in the hiring decisions. This is *detecting* it so humans can decide what to do.

---

## The Key Design Question: Where Must Humans Decide?

**Wrong approach**: "Humans make final hiring decisions."
(This is too late. Agents already filtered 80% of candidates. Humans inherit biased shortlists.)

**Better approach**: Break hiring into decision gates. Identify which gates *must* be human.

```
Gate 1: Query Interpretation
  Q: "I want people just like our current team"
  A: [HUMAN MUST DECIDE] Is this legal intent?
  Why: Homogeneity + "just like" is often proxy for discrimination

Gate 2: Candidate Search
  Q: "Find candidates matching criteria"
  A: [AGENT] Searches, ranks by relevance, audits fairness
  Why: Scale problem. Agents good at searching.
       But audit must be background, not filtering.

Gate 3: Fairness Review
  Q: "Is this decision disparately impactful?"
  A: [AGENT] Runs audit, flags impacts
       [HUMAN DECIDES] "Is this acceptable?"
  Why: Impact threshold is policy, not technical.

Gate 4: Candidate Assessment
  Q: "Will this person succeed in role?"
  A: [AGENT] Prepares assessment + explanations
       [HUMAN DECIDES] "Do I believe this?"
  Why: Judgment calls require human experience.

Gate 5: Offer & Onboarding
  A: [AGENT] Creates accounts, sends offer, schedules onboarding
       [HUMAN POINT] Offer negotiation (if needed)
  Why: Once a human approved, agents can execute.
```

**The Real Cost**
If you put humans in all 5 gates, hiring is slow.
If you remove humans from gates 1, 3, you're building liability.

LinkedIn's answer: Humans at gates 1, 3, 4. Agents automate gates 2, 5.
Cost: ~2 hours per hire. Benefit: Zero discrimination claims, defensible decisions, candidate trust.

---

## Cross-Domain Lessons

### **1. Scale Amplifies Bias**
A biased heuristic affects 10 people/week if a human uses it.
The same heuristic in an agent affects 1,000 people/week.
If you're going to automate, build fairness in from the start.

### **2. Explainability Is Risk Management, Not Nice-to-Have**
You can't defend "the AI decided" in court.
You *can* defend "We assessed candidates against these 7 criteria, your resume matched 5, and here's why we're advancing others."

### **3. Feedback Loops Encode Historical Bias**
Training on "successful hires" teaches the model to hire people like past successful hires.
You *must* include counterfactual data: "People we didn't hire who would have succeeded."

### **4. Data Isolation Matters More Than Fairness Algorithms**
Don't let agents touch protected class data, even with fairness constraints.
It's architecturally cleaner and legally safer.

### **5. Audit Disparate Impact, Don't Pre-filter**
Run fairness audits *alongside* ranking, not *before* ranking.
Let humans decide whether impact is acceptable.
Pre-filtering is affirmative action (legal in some contexts, not all).

---

## Further Reading

- Bolukbasi et al., "Man is to Computer Programmer as Woman is to Homemaker" — classic paper on word embeddings encoding gender bias
- Obermeyer et al., "Disparate Impact on Bias in Machine Learning" — Harvard/Stanford on feedback loops
- LinkedIn's "Fairness in Hiring" white paper (2021) — their approach to audit systems
- Amazon's recruiting agent story (2018) — case study in how NOT to build this
