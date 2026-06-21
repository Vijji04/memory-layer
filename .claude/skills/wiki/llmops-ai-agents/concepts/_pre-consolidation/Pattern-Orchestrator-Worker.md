---
title: Pattern: Orchestrator-Worker
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, patterns, orchestration, case-studies]
confidence: high
source_files: 1
---

# Pattern: Orchestrator-Worker

When a problem is too complex for a single agent, split it. **Orchestrator agents decompose** hard problems into independent subproblems, dispatch each to a **specialist worker agent**, collect results, and synthesize. This pattern scales reasoning: one agent can't answer "given these three data sources, portfolio risk, and regulatory constraints, what product should I recommend?", but an orchestrator routing to [Data Analyst, Risk Officer, Compliance Officer, Recommendation Engine] can.

The core challenge: **managing context and communication cost**. Each worker needs enough context to solve its problem, but not so much that you blow token budgets. Workers operate in isolation (good: parallelizable, modular) but need shared context (bad: must pass state, enforce contracts).

---

## Case Study 1: Yahoo! Finance — Multi-Agent Financial Research

### The Business Problem

A user asks Yahoo! Finance: "Should I buy Apple stock now? Consider recent market conditions, the company's latest earnings, and current valuations."

This needs:
1. **Data Retrieval Agent**: fetch current Apple stock price, market indices, historical returns
2. **News Analysis Agent**: recent earnings report, any major news, sentiment analysis
3. **Financial Modeling Agent**: DCF valuation, peer comparison, growth projections
4. **Risk Assessment Agent**: volatility, correlation with portfolio, downside scenarios

No single LLM can do all this reliably. Missing data? Biased analysis? Wrong valuation model? The more complex the problem, the more specialization helps.

Yahoo! Finance built a **multi-agent research platform** where:
1. **Orchestrator** reads the user question, decomposes into sub-tasks
2. **Workers** execute in parallel: retrieve data, analyze news, model financials, assess risk
3. **Orchestrator** synthesizes results into a final recommendation with confidence level

The system handles 100,000+ queries per day. Quality is measured by user engagement (did they act on the recommendation?) and outcomes (did the recommendation age well?).

### Why This Pattern Fits

**Orchestrator-worker solves the specialization problem**:
- Complex problems decompose naturally into subproblems
- Each subproblem has specialized expertise, data sources, tools
- Workers are modular: easy to update one without affecting others
- Parallel execution: if tasks are independent, run concurrently
- Clear contracts: orchestrator defines what each worker must provide

Different from previous patterns:
- Not RAG (no single retrieval source)
- Not conversational (no user interruptions)
- Not autonomous action (no external systems to update)
- Here: reasoning complexity requires decomposition

### Architecture Diagram

```
┌──────────────────────────────────────────────┐
│  User Query                                  │
│  "Should I buy Apple stock now?"             │
└────────────────┬─────────────────────────────┘
                 │
        ┌────────▼─────────────┐
        │  Orchestrator Agent  │
        │                      │
        │  Parse query:        │
        │  - Company: Apple    │
        │  - Task: Buy decision│
        │  - Context: market   │
        │                      │
        │  Decompose into:     │
        │  ├─ Get current data │
        │  ├─ Analyze news     │
        │  ├─ Value company    │
        │  └─ Assess risk      │
        └────────┬─────────────┘
                 │
        ┌────────┴───────────────────────┬────────────────────┬─────────────┐
        │                                │                    │             │
    ┌───▼────────┐  ┌──────────────┐  ┌─▼──────────┐  ┌────▼──────────┐
    │ Data Agent │  │ News Agent   │  │Value Agent │  │ Risk Agent    │
    │            │  │              │  │            │  │               │
    │ 1. Fetch   │  │ 1. Headlines │  │ 1. Get     │  │ 1. Volatility │
    │    price   │  │ 2. Sentiment │  │    financ  │  │ 2. Drawdown   │
    │ 2. Indices │  │ 3. Impact    │  │ 2. DCF     │  │ 3. Correl.    │
    │ 3. History │  │              │  │ 3. Comps   │  │ 4. Scenarios  │
    │            │  │              │  │            │  │               │
    │ Output:    │  │ Output:      │  │ Output:    │  │ Output:       │
    │ {price,    │  │ {sentiment,  │  │ {fair_val, │  │ {vol, beta,   │
    │  indices,  │  │  events,     │  │  range}    │  │  scenarios}   │
    │  returns}  │  │  confidence} │  │            │  │               │
    └───┬────────┘  └──────┬───────┘  └─┬──────────┘  └────┬──────────┘
        │                  │            │                  │
        └──────────────────┴────────────┴──────────────────┘
                           │
        ┌──────────────────▼───────────────────────┐
        │  Orchestrator: Synthesis                 │
        │                                          │
        │  Combine outputs:                        │
        │  • Current price: $182                   │
        │  • News: Mixed (earnings beat, macro)    │
        │  • Fair value: $190-200 (DCF)           │
        │  • Risk: Moderate volatility, -15% scenario │
        │                                          │
        │  Generate recommendation:                │
        │  HOLD with UPSIDE (fair value > price)  │
        │  But watch macro risks                   │
        │  Confidence: 0.72                        │
        └────────────────────────────────────────┘
```

### Implementation: Key Components

#### 1. Orchestrator Decomposition

```python
from typing import List, Dict
import anthropic
import json

@dataclass
class WorkTask:
    """Definition of work for a specialist agent."""
    task_id: str
    worker_type: str  # 'data', 'news', 'valuation', 'risk'
    query: str
    context: Dict  # Shared context: ticker, date, etc.
    expected_output_schema: Dict  # What worker must return

class OrchestratorAgent:
    """
    Main orchestrator: parses user query, decomposes into tasks,
    coordinates workers, synthesizes result.
    """
    
    def __init__(self, worker_agents: Dict[str, any]):
        """
        worker_agents: Dict mapping worker type to worker class
        e.g., {'data': DataAgent(), 'news': NewsAgent(), ...}
        """
        self.workers = worker_agents
        self.client = anthropic.Anthropic()
    
    def answer_question(self, query: str) -> Dict:
        """
        End-to-end: decompose -> execute -> synthesize
        """
        
        # Step 1: Parse query to extract structured intent
        intent = self._parse_query(query)
        print(f"[Orchestrator] Parsed intent: {json.dumps(intent, indent=2)}")
        
        # Step 2: Decompose into tasks
        tasks = self._decompose(intent)
        print(f"[Orchestrator] Created {len(tasks)} tasks")
        
        # Step 3: Execute tasks (in parallel or sequential)
        task_results = self._execute_tasks(tasks)
        
        # Step 4: Synthesize results into final answer
        final_answer = self._synthesize(intent, task_results)
        
        return {
            'answer': final_answer['answer'],
            'confidence': final_answer['confidence'],
            'sources': final_answer['sources'],
            'reasoning': final_answer['reasoning']
        }
    
    def _parse_query(self, query: str) -> Dict:
        """
        Extract structured intent from free-form query.
        
        Returns:
            {
                'company': 'Apple',
                'ticker': 'AAPL',
                'question_type': 'buy_decision',
                'context': ['market_conditions', 'earnings', 'valuation'],
                'time_horizon': 'short_term',
                'risk_tolerance': 'unknown'
            }
        """
        
        prompt = f"""Parse this investment query into structured intent.

Query: "{query}"

Extract:
1. Company name
2. Stock ticker
3. Question type (buy/sell/hold decision, valuation, risk, etc.)
4. Context factors mentioned (market, earnings, valuation, etc.)
5. Implied time horizon and risk tolerance

Respond with JSON:
{{
    "company": "<name>",
    "ticker": "<TICKER>",
    "question_type": "<type>",
    "context_factors": [<list>],
    "time_horizon": "<short_term|medium|long_term>",
    "risk_tolerance": "<unknown|low|medium|high>"
}}"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            return json.loads(response.content[0].text)
        except:
            return {'company': 'Unknown', 'ticker': 'UNKNOWN'}
    
    def _decompose(self, intent: Dict) -> List[WorkTask]:
        """
        Decompose into independent tasks for workers.
        """
        
        ticker = intent.get('ticker', '')
        context = {
            'ticker': ticker,
            'company': intent.get('company'),
            'date': self._get_today(),
            'time_horizon': intent.get('time_horizon')
        }
        
        tasks = []
        
        # Always needed: current data
        tasks.append(WorkTask(
            task_id='data_1',
            worker_type='data',
            query=f"Get current price, market indices, and historical returns for {ticker}",
            context=context,
            expected_output_schema={
                'current_price': 'float',
                'market_indices': 'dict',
                'historical_returns': 'dict'
            }
        ))
        
        # News/sentiment analysis
        tasks.append(WorkTask(
            task_id='news_1',
            worker_type='news',
            query=f"Analyze recent news and earnings for {intent.get('company')}. What's the sentiment?",
            context=context,
            expected_output_schema={
                'recent_news': 'list',
                'sentiment': 'float (-1 to 1)',
                'key_events': 'list'
            }
        ))
        
        # Valuation
        tasks.append(WorkTask(
            task_id='valuation_1',
            worker_type='valuation',
            query=f"Determine fair value for {ticker} using DCF and comparable companies",
            context=context,
            expected_output_schema={
                'dcf_value': 'float',
                'comparable_range': 'tuple (min, max)',
                'fair_value_estimate': 'float'
            }
        ))
        
        # Risk assessment
        tasks.append(WorkTask(
            task_id='risk_1',
            worker_type='risk',
            query=f"Assess risk for {ticker}: volatility, beta, downside scenarios",
            context=context,
            expected_output_schema={
                'volatility': 'float',
                'beta': 'float',
                'downside_scenario_pct': 'float',
                'risk_rating': 'string'
            }
        ))
        
        return tasks
    
    def _execute_tasks(self, tasks: List[WorkTask]) -> Dict[str, Dict]:
        """
        Execute all tasks (in practice, in parallel).
        Collect results indexed by task_id.
        """
        
        results = {}
        
        for task in tasks:
            print(f"[Orchestrator] Executing {task.task_id} ({task.worker_type})")
            
            # Get appropriate worker
            worker = self.workers.get(task.worker_type)
            if not worker:
                results[task.task_id] = {'error': f'No worker for {task.worker_type}'}
                continue
            
            # Execute task
            try:
                result = worker.execute(task)
                results[task.task_id] = result
            except Exception as e:
                results[task.task_id] = {'error': str(e)}
        
        return results
    
    def _synthesize(
        self,
        intent: Dict,
        task_results: Dict[str, Dict]
    ) -> Dict:
        """
        Combine worker outputs into final recommendation.
        """
        
        # Build context from all worker outputs
        synthesis_prompt = f"""You are a senior investment analyst. Synthesize these research findings
into a buy/hold/sell recommendation.

RESEARCH FINDINGS:
"""
        
        # Add data findings
        if 'data_1' in task_results:
            data = task_results['data_1']
            synthesis_prompt += f"""
Current Data:
- Price: ${data.get('current_price')}
- Market: {json.dumps(data.get('market_indices'))}
- Returns (YTD): {data.get('historical_returns', {}).get('ytd_return')}%
"""
        
        # Add news findings
        if 'news_1' in task_results:
            news = task_results['news_1']
            synthesis_prompt += f"""
News & Sentiment:
- Recent events: {', '.join(news.get('key_events', []))}
- Sentiment score: {news.get('sentiment')} (from -1=very negative to 1=very positive)
"""
        
        # Add valuation findings
        if 'valuation_1' in task_results:
            val = task_results['valuation_1']
            synthesis_prompt += f"""
Valuation:
- DCF Fair Value: ${val.get('dcf_value')}
- Comparable Range: ${val.get('comparable_range', [0,0])[0]} - ${val.get('comparable_range', [0,0])[1]}
- Best Estimate: ${val.get('fair_value_estimate')}
"""
        
        # Add risk findings
        if 'risk_1' in task_results:
            risk = task_results['risk_1']
            synthesis_prompt += f"""
Risk Profile:
- Volatility (annual): {risk.get('volatility')}%
- Beta: {risk.get('beta')}
- Downside scenario: {risk.get('downside_scenario_pct')}%
"""
        
        synthesis_prompt += """

TASK: Generate recommendation with:
1. Clear direction (BUY/HOLD/SELL)
2. Primary rationale (2-3 sentences)
3. Key risks to watch
4. Confidence level (0-1)
5. Time horizon for recommendation

Format as JSON:
{
    "recommendation": "BUY|HOLD|SELL",
    "rationale": "<reason>",
    "key_risks": ["<risk1>", "<risk2>"],
    "confidence": <0-1>,
    "time_horizon": "<short|medium|long>"
}"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=600,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )
        
        try:
            result = json.loads(response.content[0].text)
        except:
            result = {
                'recommendation': 'HOLD',
                'rationale': 'Insufficient data for recommendation',
                'confidence': 0.3
            }
        
        return {
            'answer': f"{result['recommendation']}: {result['rationale']}",
            'confidence': result.get('confidence', 0.5),
            'sources': list(task_results.keys()),
            'reasoning': json.dumps(result, indent=2)
        }
    
    def _get_today(self) -> str:
        from datetime import date
        return str(date.today())

# Usage
class DataAgent:
    """Example worker: fetches data."""
    def execute(self, task: WorkTask) -> Dict:
        # Stub; in production, would query real APIs
        return {
            'current_price': 182.45,
            'market_indices': {'spy': 5123, 'tech_etf': 3421},
            'historical_returns': {'ytd_return': 12.3, 'one_year': 28.5}
        }

class NewsAgent:
    """Example worker: analyzes news."""
    def execute(self, task: WorkTask) -> Dict:
        return {
            'key_events': ['Beat earnings expectations', 'Vision Pro sales slower than expected'],
            'sentiment': 0.3,  # Slightly positive
            'confidence': 0.75
        }

class ValuationAgent:
    """Example worker: values company."""
    def execute(self, task: WorkTask) -> Dict:
        return {
            'dcf_value': 195.0,
            'comparable_range': (185, 210),
            'fair_value_estimate': 192.5
        }

class RiskAgent:
    """Example worker: assesses risk."""
    def execute(self, task: WorkTask) -> Dict:
        return {
            'volatility': 21.5,
            'beta': 1.2,
            'downside_scenario_pct': -15,
            'risk_rating': 'moderate'
        }

# Setup and run
orchestrator = OrchestratorAgent({
    'data': DataAgent(),
    'news': NewsAgent(),
    'valuation': ValuationAgent(),
    'risk': RiskAgent()
})

result = orchestrator.answer_question(
    "Should I buy Apple stock now? Consider recent earnings and market conditions."
)

print(f"\nFinal Answer: {result['answer']}")
print(f"Confidence: {result['confidence']:.2f}")
```

#### 2. Worker Agent Contract & Validation

```python
from typing import Any

class WorkerContract:
    """
    Define expected input/output for a worker.
    
    Ensures:
    - Worker receives complete context
    - Worker output matches schema
    - Orchestrator can validate output
    """
    
    def __init__(self, worker_type: str, input_schema: Dict, output_schema: Dict):
        self.worker_type = worker_type
        self.input_schema = input_schema
        self.output_schema = output_schema
    
    def validate_input(self, task: WorkTask) -> bool:
        """Check that task provides all required input."""
        for field, field_type in self.input_schema.items():
            if field not in task.context:
                print(f"Warning: Missing {field} in task context")
        return True
    
    def validate_output(self, output: Dict) -> Tuple[bool, List[str]]:
        """Check that output matches expected schema."""
        errors = []
        
        for field, expected_type in self.output_schema.items():
            if field not in output:
                errors.append(f"Missing field: {field}")
            elif not self._type_matches(output[field], expected_type):
                errors.append(f"Field {field} type mismatch. Expected {expected_type}, got {type(output[field])}")
        
        return len(errors) == 0, errors
    
    def _type_matches(self, value: Any, expected: str) -> bool:
        """Simple type checking."""
        type_map = {
            'float': float,
            'int': int,
            'str': str,
            'dict': dict,
            'list': list,
            'bool': bool
        }
        
        expected_type = type_map.get(expected, object)
        return isinstance(value, expected_type) or expected == 'any'

# Define contracts for each worker type
CONTRACTS = {
    'data': WorkerContract(
        worker_type='data',
        input_schema={
            'ticker': 'str',
            'date': 'str'
        },
        output_schema={
            'current_price': 'float',
            'market_indices': 'dict',
            'historical_returns': 'dict'
        }
    ),
    'news': WorkerContract(
        worker_type='news',
        input_schema={
            'company': 'str',
            'date': 'str'
        },
        output_schema={
            'key_events': 'list',
            'sentiment': 'float',
            'confidence': 'float'
        }
    ),
    'valuation': WorkerContract(
        worker_type='valuation',
        input_schema={
            'ticker': 'str',
            'current_price': 'float'
        },
        output_schema={
            'dcf_value': 'float',
            'comparable_range': 'tuple',
            'fair_value_estimate': 'float'
        }
    ),
    'risk': WorkerContract(
        worker_type='risk',
        input_schema={
            'ticker': 'str',
            'time_horizon': 'str'
        },
        output_schema={
            'volatility': 'float',
            'beta': 'float',
            'downside_scenario_pct': 'float',
            'risk_rating': 'str'
        }
    )
}

# Usage in orchestrator
def _validate_worker_output(
    self,
    task_id: str,
    worker_type: str,
    output: Dict
) -> Tuple[bool, List[str]]:
    """Validate worker output against contract."""
    
    contract = CONTRACTS.get(worker_type)
    if not contract:
        return False, [f"No contract defined for {worker_type}"]
    
    valid, errors = contract.validate_output(output)
    
    if not valid:
        print(f"[Orchestrator] {task_id} validation failed:")
        for error in errors:
            print(f"  - {error}")
    
    return valid, errors
```

#### 3. Context Management & Token Optimization

```python
class ContextManager:
    """
    Manage shared context across orchestrator and workers.
    
    Challenge: Keep workers independent but minimize redundant context passing.
    Solution: Shared context indexed by key (ticker, date, etc.),
    each worker gets only what it needs.
    """
    
    def __init__(self):
        self.shared_context = {}
        self.worker_contexts = {}  # Per-worker views
    
    def set_shared_context(self, key: str, value: Any):
        """Set value in shared context."""
        self.shared_context[key] = value
    
    def get_worker_context(
        self,
        worker_type: str,
        fields: List[str]
    ) -> Dict:
        """
        Build minimal context for a specific worker.
        
        Only include fields the worker needs.
        """
        worker_context = {}
        
        for field in fields:
            if field in self.shared_context:
                worker_context[field] = self.shared_context[field]
        
        return worker_context
    
    def estimate_token_usage(self, context: Dict) -> int:
        """Rough estimate of tokens in context."""
        # Simplified; ~4 chars per token on average
        context_str = json.dumps(context)
        return len(context_str) // 4
    
    def optimize_context(self, target_tokens: int = 2000):
        """
        Reduce context size if it exceeds target.
        
        Priorities:
        1. Keep structured data (prices, metrics)
        2. Prune verbose text (full articles, histories)
        3. Summarize what must be kept
        """
        
        current_tokens = self.estimate_token_usage(self.shared_context)
        
        if current_tokens <= target_tokens:
            return  # OK
        
        print(f"[ContextManager] Optimizing: {current_tokens} tokens -> {target_tokens}")
        
        # Priority: prune low-value fields
        low_priority = ['full_articles', 'comment_history', 'all_historical_data']
        
        for field in low_priority:
            if field in self.shared_context:
                del self.shared_context[field]
                new_tokens = self.estimate_token_usage(self.shared_context)
                if new_tokens <= target_tokens:
                    print(f"[ContextManager] Optimized: {new_tokens} tokens")
                    return
        
        # If still over, summarize text fields
        text_fields = [k for k, v in self.shared_context.items() if isinstance(v, str)]
        for field in text_fields:
            text = self.shared_context[field]
            if len(text) > 500:
                # Truncate with ellipsis
                self.shared_context[field] = text[:300] + "..."
        
        print(f"[ContextManager] Optimized (reduced text fields)")

# Usage
ctx = ContextManager()

# Shared context: available to all workers
ctx.set_shared_context('ticker', 'AAPL')
ctx.set_shared_context('current_date', '2026-04-23')
ctx.set_shared_context('current_price', 182.45)
ctx.set_shared_context('market_cap', 2.8e12)

# Each worker gets only what it needs
data_worker_context = ctx.get_worker_context('data', ['ticker', 'current_date'])
news_worker_context = ctx.get_worker_context('news', ['ticker', 'current_date'])
risk_worker_context = ctx.get_worker_context('risk', ['ticker', 'current_price'])

print(f"Data worker gets {ctx.estimate_token_usage(data_worker_context)} tokens")
print(f"News worker gets {ctx.estimate_token_usage(news_worker_context)} tokens")
```

### Design Decisions & Why

**1. Why Orchestrator, Not Monolithic Agent?**
- Single agent trying to do data retrieval, news analysis, valuation, AND risk assessment is mediocre at all
- Specialized agents are deep experts: DataAgent knows APIs, NewsAgent knows sentiment analysis, etc.
- Parallel execution: if tasks are independent, run concurrently (saves latency)
- Modularity: update one worker without affecting others

**2. Why Contracts Between Orchestrator & Workers?**
- Ensures workers receive complete context (otherwise they hallucinate)
- Ensures orchestrator validates output (bad data propagates silently without validation)
- Clear interface: workers know what to return, orchestrator knows what to expect
- Testable: can test each worker in isolation

**3. Why Shared Context Rather Than Duplicate Context?**
- Naive approach: pass all context to every worker (massive token waste)
- Better: shared context indexed by key, each worker pulls what it needs
- Token optimization: estimate usage, prune low-priority fields if over budget
- Fail gracefully: if worker needs data that's not in context, it can say so

**4. Why Synthesis Step After All Workers Finish?**
- Don't synthesize early (lose information from parallel tasks)
- Collect all results, then synthesize holistically
- Orchestrator acts as final judge: weighs evidence, calls out contradictions, makes call

### Key Takeaways

1. **Decompose complex reasoning into specialist workers**: don't expect one agent to do data, news, valuation, and risk. Specialize.

2. **Use contracts to enforce input/output expectations**: workers declare what they need and what they return. Validates automatically.

3. **Shared context beats duplicated context**: use indexed context, let workers pull what they need. Estimate token usage and optimize if needed.

4. **Parallel execution saves latency**: if tasks are independent, run them concurrently. Synthesis happens after all results arrive.

5. **Validate worker output**: bad data from one worker propagates through synthesis. Catch it early.

---

## Case Study 2: City of Buenos Aires — Government Service Assistant

### The Business Problem

Buenos Aires provides 1,300+ government services: permits, licenses, taxes, subsidies, healthcare, housing. Citizens ask:

- "How do I get a driver's license renewal?"
- "What's the procedure and fee for a business permit?"
- "Am I eligible for housing assistance?"

Each service spans multiple city departments and has different rules:
- **Licenses & Permits**: Traffic Bureau
- **Taxes**: Revenue Service
- **Social Services**: Welfare Department
- **Healthcare**: Health Ministry

Naive RAG over all documents fails: the same question might need Licenses (for ID), Revenue (for tax ID), and Welfare (for address verification). A single retrieval system can't route to the right department.

Buenos Aires built an **LLM-powered government assistant** where:
1. **Router Agent** determines which departments are relevant
2. **Specialist agents per department** answer using department-specific knowledge bases
3. **Composer Agent** synthesizes across departments
4. Escalates to human (government services always have edge cases)

The system handles 50,000+ queries per month. Goal: 80% resolved without human (some questions are inherently complex or require sign-offs).

### Why This Pattern Fits

**Cross-department routing** is an orchestrator-worker problem:
- Different departments have different knowledge bases
- A question might span multiple departments
- Department-specific rules must be enforced (licenses require ID, taxes require residence, etc.)
- Escalation to human is explicit gate

Differs from Yahoo Finance:
- Here, departments are sequential (get ID first, then license)
- There, workers were parallel (all retrieve simultaneously)
- Here, one department's output feeds into another's input

### Architecture Diagram

```
┌───────────────────────────────────────────┐
│  Citizen Query                            │
│  "How do I get a driver's license?"       │
└──────────────┬────────────────────────────┘
               │
    ┌──────────▼─────────────┐
    │  Router Agent          │
    │                        │
    │  Intent: license       │
    │  Determine departments:│
    │  1. Traffic Bureau     │
    │  2. ID Office (maybe)  │
    │  3. Health (if needed) │
    └──────────┬─────────────┘
               │
    ┌──────────▼──────────────────┐
    │ Traffic Bureau Agent        │
    │ (Specialist: licenses)      │
    │                            │
    │ Q: How to renew license?   │
    │ A: Documents needed,       │
    │    fee, timeline           │
    └──────────┬─────────────────┘
               │
    ┌──────────▼──────────────────┐
    │ ID Office Agent            │
    │ (Specialist: documents)    │
    │                            │
    │ Q: What ID needed?         │
    │ A: DNI required,           │
    │    valid through 2028      │
    └──────────┬─────────────────┘
               │
    ┌──────────▼──────────────────┐
    │ Composer Agent             │
    │ (Synthesize result)        │
    │                            │
    │ "To renew license:         │
    │  1. Get valid DNI          │
    │  2. Submit to Traffic      │
    │  3. Fee: $X                │
    │  4. Timeline: Y days"      │
    └────────────────────────────┘
```

### Implementation: Key Components

#### 1. Intent Router for Multi-Department Questions

```python
from typing import List, Set

class DepartmentRouter:
    """
    Route citizen question to relevant department(s).
    
    Challenge: Some questions span multiple departments.
    Route to all relevant departments, then sequence if needed.
    """
    
    DEPARTMENTS = {
        'traffic': {
            'name': 'Tránsito (Traffic Bureau)',
            'keywords': ['driver', 'license', 'vehicle', 'car', 'parking', 'plate'],
            'knowledge_base': 'traffic_policies.txt'
        },
        'id': {
            'name': 'Registro Nacional de Personas (ID Office)',
            'keywords': ['dni', 'document', 'passport', 'identification', 'identity'],
            'knowledge_base': 'id_policies.txt'
        },
        'taxes': {
            'name': 'Agencia de Recaudación (Revenue)',
            'keywords': ['tax', 'fee', 'payment', 'invoice', 'billing'],
            'knowledge_base': 'tax_policies.txt'
        },
        'welfare': {
            'name': 'Ministerio de Desarrollo Social (Social Services)',
            'keywords': ['subsidy', 'assistance', 'housing', 'unemployment', 'support'],
            'knowledge_base': 'welfare_policies.txt'
        },
        'health': {
            'name': 'Ministerio de Salud (Health)',
            'keywords': ['vaccine', 'health', 'doctor', 'appointment', 'medical'],
            'knowledge_base': 'health_policies.txt'
        }
    }
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def route(self, query: str) -> List[str]:
        """
        Determine which departments are relevant.
        
        Returns: List of department IDs, in processing order
        """
        
        relevant_depts = set()
        
        # Heuristic 1: Keyword matching
        query_lower = query.lower()
        for dept_id, dept_info in self.DEPARTMENTS.items():
            if any(kw in query_lower for kw in dept_info['keywords']):
                relevant_depts.add(dept_id)
        
        # Heuristic 2: LLM-based routing (if keywords miss something)
        if not relevant_depts:
            relevant_depts = self._llm_route(query)
        
        # Step 3: Sequence dependencies
        # Some departments must be queried first
        sequence = self._sequence_dependencies(relevant_depts)
        
        print(f"[Router] Query routes to: {[self.DEPARTMENTS[d]['name'] for d in sequence]}")
        
        return sequence
    
    def _llm_route(self, query: str) -> Set[str]:
        """Use LLM to determine relevant departments."""
        
        dept_list = "\n".join(
            f"- {dept_id}: {info['name']}"
            for dept_id, info in self.DEPARTMENTS.items()
        )
        
        prompt = f"""Which city departments should answer this citizen query?

Departments:
{dept_list}

Query: "{query}"

Return JSON:
{{"departments": ["dept_id1", "dept_id2"]}}"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            result = json.loads(response.content[0].text)
            return set(result.get('departments', []))
        except:
            return set()
    
    def _sequence_dependencies(self, depts: Set[str]) -> List[str]:
        """
        Order departments based on dependencies.
        
        E.g., ID Office before Traffic (need DNI before license)
        """
        
        dependency_order = ['id', 'taxes', 'traffic', 'health', 'welfare']
        
        sequenced = [d for d in dependency_order if d in depts]
        sequenced.extend([d for d in depts if d not in dependency_order])
        
        return sequenced

# Usage
router = DepartmentRouter()

relevant = router.route("I need a driver's license. What documents do I need?")
# Output: ['id', 'traffic']

relevant = router.route("Can I get housing assistance? I'm unemployed.")
# Output: ['welfare', 'id']
```

#### 2. Department-Specific Specialist Agents

```python
@dataclass
class DepartmentContext:
    """Context passed to department agents."""
    citizen_query: str
    citizen_info: Dict  # Name, ID, address, etc. (if known)
    prior_answers: Dict  # Answers from earlier departments
    department_id: str

class DepartmentAgent:
    """Base class for department-specific agent."""
    
    def __init__(self, dept_id: str, knowledge_base_path: str):
        self.dept_id = dept_id
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.client = anthropic.Anthropic()
    
    def answer(self, context: DepartmentContext) -> Dict:
        """
        Answer citizen query using department knowledge base.
        
        Optionally use prior answers from other departments.
        """
        
        # Build prompt with department knowledge
        kb_text = self._format_knowledge_base()
        
        prior_context = ""
        if context.prior_answers:
            prior_context = "Prior information from other departments:\n"
            for dept, answer in context.prior_answers.items():
                prior_context += f"- {dept}: {answer}\n"
        
        prompt = f"""You are a specialist for {self.dept_id} in Buenos Aires city government.
Answer the citizen's question using your knowledge base.

KNOWLEDGE BASE:
{kb_text}

{prior_context}

CITIZEN QUERY: {context.citizen_query}

Provide a clear, actionable answer:
1. What the citizen needs
2. Documents/requirements
3. Fee (if applicable)
4. Timeline
5. Contact info or next steps

If you cannot answer with your knowledge base, indicate what information is missing."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer_text = response.content[0].text
        
        return {
            'department': self.dept_id,
            'answer': answer_text,
            'confidence': self._estimate_confidence(answer_text),
            'requires_human': self._should_escalate(answer_text)
        }
    
    def _load_knowledge_base(self, path: str) -> str:
        """Load department policies/procedures."""
        try:
            with open(path) as f:
                return f.read()
        except:
            return "(Knowledge base not loaded)"
    
    def _format_knowledge_base(self) -> str:
        """Format KB for LLM."""
        # In production, would section by topic, create index, etc.
        return self.knowledge_base[:2000]  # First 2000 chars
    
    def _estimate_confidence(self, answer: str) -> float:
        """Estimate confidence in answer."""
        if "cannot" in answer.lower() or "unknown" in answer.lower():
            return 0.5
        return 0.8
    
    def _should_escalate(self, answer: str) -> bool:
        """Check if answer requires human review."""
        escalation_phrases = [
            'special circumstances',
            'exception',
            'requires approval',
            'needs human review',
            'contact your local office'
        ]
        return any(phrase in answer.lower() for phrase in escalation_phrases)

# Implement specific agents
class TrafficAgent(DepartmentAgent):
    def __init__(self):
        super().__init__('traffic', 'data/traffic_policies.txt')

class IDAgent(DepartmentAgent):
    def __init__(self):
        super().__init__('id', 'data/id_policies.txt')

class WelfareAgent(DepartmentAgent):
    def __init__(self):
        super().__init__('welfare', 'data/welfare_policies.txt')

# Usage
traffic_agent = TrafficAgent()
id_agent = IDAgent()

# Query ID office first
id_context = DepartmentContext(
    citizen_query="Do I need a valid ID to get a driver's license?",
    citizen_info={},
    prior_answers={},
    department_id='id'
)

id_answer = id_agent.answer(id_context)
print(f"ID Office: {id_answer['answer']}")

# Then query Traffic, passing ID answer as context
traffic_context = DepartmentContext(
    citizen_query="What documents do I need for a driver's license renewal?",
    citizen_info={},
    prior_answers={'id': id_answer['answer']},
    department_id='traffic'
)

traffic_answer = traffic_agent.answer(traffic_context)
print(f"\nTraffic Bureau: {traffic_answer['answer']}")
```

#### 3. Response Composer & Escalation Gate

```python
class ResponseComposer:
    """
    Synthesize answers from multiple departments.
    Present cohesive response to citizen.
    Escalate if necessary.
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def compose(
        self,
        original_query: str,
        department_answers: List[Dict],
        router: DepartmentRouter
    ) -> Dict:
        """
        Combine department answers into single citizen response.
        """
        
        # Check if escalation is needed
        escalation_reasons = [
            ans.get('requires_human')
            for ans in department_answers
            if ans.get('requires_human')
        ]
        
        if escalation_reasons:
            return self._escalate(original_query, department_answers)
        
        # Synthesize answers
        synthesis_prompt = f"""Synthesize these government department answers into a clear response for a citizen.

ORIGINAL QUERY: {original_query}

DEPARTMENT ANSWERS:
"""
        
        for ans in department_answers:
            synthesis_prompt += f"\n{ans['department']}:\n{ans['answer']}\n"
        
        synthesis_prompt += """
Create a unified, easy-to-follow response that:
1. Answers the citizen's question
2. Lists all documents needed
3. Explains the step-by-step process
4. Provides fees and timeline
5. Gives contact info

Format for a citizen (not jargon-heavy)."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )
        
        final_answer = response.content[0].text
        
        return {
            'status': 'answered',
            'answer': final_answer,
            'sources': [ans['department'] for ans in department_answers],
            'confidence': sum(ans.get('confidence', 0.5) for ans in department_answers) / len(department_answers)
        }
    
    def _escalate(
        self,
        query: str,
        department_answers: List[Dict]
    ) -> Dict:
        """
        Escalate to human agent.
        """
        
        summary = "Department answers:\n"
        for ans in department_answers:
            if ans.get('requires_human'):
                summary += f"- {ans['department']}: REQUIRES HUMAN REVIEW\n"
        
        return {
            'status': 'escalated',
            'reason': summary,
            'message': "Your question requires assistance from a government specialist. A human agent will contact you within 24 hours.",
            'ticket_id': f"GOV_{hash(query) % 100000}"
        }

# Usage
composer = ResponseComposer()

all_answers = [
    id_answer,
    traffic_answer
]

final = composer.compose(
    original_query="How do I get a driver's license?",
    department_answers=all_answers,
    router=router
)

if final['status'] == 'answered':
    print(f"\nFINAL ANSWER:\n{final['answer']}")
else:
    print(f"\nEscalated: {final['reason']}")
    print(f"Ticket: {final['ticket_id']}")
```

### Design Decisions & Why

**1. Why Sequential Routing Instead of Parallel?**
- Some questions span departments but have dependencies
- ID Office must answer first (citizen needs valid ID)
- Traffic Bureau uses ID's answer
- Sequential ensures prior answers feed into later queries

**2. Why Department-Specific Knowledge Bases?**
- Traffic has different rules than Welfare
- Policy updates happen per-department
- Easier to audit (which version of policy did this answer use?)
- Supports partial failures (if Traffic KB is outdated, Welfare still works)

**3. Why Separate Escalation Logic?**
- Some questions are legitimately complex (multiple conditions, exceptions)
- Don't force LLM to guess; escalate to human
- Clear criteria: if LLM says "requires human review", escalate
- Prevents bad answers that sound confident but are wrong

### Key Takeaways

1. **Route to multiple departments when needed**: don't assume single department has answer. Router determines relevant departments.

2. **Sequence dependencies explicitly**: if Department B needs output from Department A, query A first.

3. **Department agents have isolation + context**: each agent is independent specialist with own KB, but can read prior answers from other departments.

4. **Escalate early**: if any department says it needs human, escalate entire query. One uncertain answer ≠ escalate; one that needs sign-off = escalate.

5. **Compose across departments**: final answer synthesizes all department input. Citizen sees one clear answer, not fragmented responses.

---

## Case Study 3: Prudential — Multi-Agent Platform for Financial Advisors

### The Business Problem

Prudential serves 100,000+ financial advisors. Each advisor manages portfolios for clients and needs to provide recommendations on:

- **Client data analysis**: income, risk tolerance, goals
- **Market intelligence**: equity/bond valuations, economic outlook
- **Risk profiling**: concentration, correlation, downside scenarios
- **Product recommendations**: which products fit this client's profile
- **Compliance check**: is recommendation legally compliant, documented

A manual recommendation takes an advisor 1-2 hours. Multiply by 100,000 advisors × 10+ recommendations per day = massive workload. Prudential built a **multi-agent platform** where advisors get automated recommendations + reasoning within seconds.

The system:
1. **Client Data Agent** extracts goals, constraints, risk tolerance
2. **Market Agent** fetches current valuations, economic indicators
3. **Risk Profiling Agent** calculates portfolio risk metrics
4. **Product Recommendation Agent** suggests products
5. **Compliance Agent** verifies recommendation meets regulations
6. **Advisor Dashboard** displays recommendation + reasoning

Result: 80% of routine client reviews can be auto-recommended. Advisor reviews output and approves (or refines manually). Reduces recommendation time from 1-2 hours to 15-20 minutes.

### Why This Pattern Fits

**Microservices-style agent architecture** with shared context:
- Each agent is independent service (call them in any order)
- Agents share context via message bus
- No agent is blocked waiting for another (async)
- Central orchestrator coordinates and serves advisor dashboard

Differs from prior examples:
- Parallel execution (like Yahoo Finance)
- Shared microservices context (like Buenos Aires)
- Real-time serving (like Booking conversational, but async backend)

### Architecture Diagram

```
┌─────────────────────────────────────┐
│  Advisor Requests Recommendation    │
│  (via Prudential dashboard)         │
└────────────┬────────────────────────┘
             │
    ┌────────▼─────────────┐
    │  Orchestrator        │
    │  (Message Router)    │
    │                      │
    │  1. Load client data │
    │  2. Spawn agents     │
    │  3. Wait for results │
    │  4. Compose report   │
    └────────┬─────────────┘
             │
    ┌────────┴──────────────────────────────────────────┐
    │                                                   │
 ┌──▼───────────┐  ┌──────────────┐  ┌───────────────┐ │
 │Client Data   │  │Market Data   │  │Risk Profiling │ │
 │Agent         │  │Agent         │  │Agent          │ │
 │              │  │              │  │               │ │
 │ Read:        │  │ Fetch:       │  │ Calculate:    │ │
 │ - Client DB  │  │ - Equity val │  │ - Portfolio  │ │
 │ - Goals      │  │ - Bond yield │  │   risk       │ │
 │ - Risk pref  │  │ - GDP outlook│  │ - Volatility │ │
 │              │  │              │  │ - Correlation│ │
 │ Output:      │  │ Output:      │  │               │ │
 │ {goals,      │  │ {valuations, │  │ Output:      │ │
 │  constraints}│  │  indicators} │  │ {risk_score} │ │
 └──┬───────────┘  └──────┬───────┘  └────────┬──────┘ │
    │                     │                    │        │
    └─────────────────────┴────────────────────┘        │
                      │                                 │
    ┌─────────────────▼────────────────────┐            │
    │ Shared Context Message Bus           │            │
    │ {client, market, risk_profile, ...}  │            │
    └──────────────────┬────────────────────┘            │
                       │                                 │
    ┌──────────────────┴──────────────────┐              │
    │                                     │              │
 ┌──▼──────────────┐  ┌──────────────────▼───┐         │
 │Product Recommendation Agent             Compliance  │
 │                                         Agent        │
 │ Input: {client, market, risk_profile}   │          │
 │                                         │ Check:   │
 │ Output: [{product_1, score_1},          │ - Fiduciary  │
 │          {product_2, score_2}, ...]     │ - Suitability
 │                                         │ - Document  │
 │                                         │ Output:     │
 │                                         │ APPROVED    │
 │                                         │ or FAILED   │
 └──┬──────────────────────────┬───────────┴───────────┘
    │                          │
    └──────────────┬───────────┘
                   │
        ┌──────────▼───────────┐
        │ Advisor Dashboard    │
        │                      │
        │ Recommendation:      │
        │ - Top 3 products     │
        │ - Why (reasoning)    │
        │ - Risk score         │
        │ - Compliance: ✓      │
        │                      │
        │ Advisor approves or  │
        │ modifies             │
        └──────────────────────┘
```

### Implementation: Key Components

#### 1. Message-Based Context Sharing

```python
import asyncio
from typing import Any, Callable
from datetime import datetime

class ContextMessage:
    """Message on the context bus."""
    
    def __init__(self, agent_id: str, data: Dict, timestamp: str = None):
        self.agent_id = agent_id
        self.data = data
        self.timestamp = timestamp or datetime.utcnow().isoformat()

class ContextBus:
    """
    Shared message bus for agents to exchange context.
    
    Agents publish their results; others subscribe and consume.
    """
    
    def __init__(self):
        self.context = {}  # Shared context dict
        self.subscriptions = {}  # agent_id -> callback
        self.message_log = []  # Audit trail
    
    async def publish(self, message: ContextMessage):
        """
        Publish context from an agent.
        """
        self.context.update(message.data)
        self.message_log.append(message)
        
        print(f"[ContextBus] {message.agent_id} published: {list(message.data.keys())}")
        
        # Notify subscribers
        for subscriber_id, callback in self.subscriptions.items():
            if subscriber_id != message.agent_id:  # Don't notify self
                await callback(message)
    
    def subscribe(self, agent_id: str, callback: Callable):
        """
        Subscribe to context updates.
        """
        self.subscriptions[agent_id] = callback
    
    def get_context(self) -> Dict:
        """Get current shared context."""
        return self.context.copy()
    
    def get_agent_context(self, agent_id: str, fields: List[str]) -> Dict:
        """Get only fields this agent needs."""
        return {k: self.context[k] for k in fields if k in self.context}

class AsyncAgent:
    """
    Async agent that operates independently but shares context via bus.
    """
    
    def __init__(self, agent_id: str, context_bus: ContextBus):
        self.agent_id = agent_id
        self.bus = context_bus
        self.bus.subscribe(agent_id, self._on_context_update)
    
    async def _on_context_update(self, message: ContextMessage):
        """Called when other agents publish context."""
        pass  # Override in subclass to react to updates
    
    async def publish(self, data: Dict):
        """Publish results to context bus."""
        message = ContextMessage(self.agent_id, data)
        await self.bus.publish(message)

# Concrete agents
class ClientDataAgent(AsyncAgent):
    async def execute(self):
        """Fetch and process client data."""
        await asyncio.sleep(0.5)  # Simulate work
        
        client_data = {
            'client_id': 'cli_12345',
            'age': 45,
            'income': 150000,
            'risk_tolerance': 0.6,  # 0=conservative, 1=aggressive
            'goals': ['retirement', 'college_fund'],
            'time_horizon_years': 20,
            'existing_portfolio_value': 500000
        }
        
        await self.publish({'client': client_data})
        print(f"[{self.agent_id}] Published client data")

class MarketDataAgent(AsyncAgent):
    async def execute(self):
        """Fetch market data."""
        await asyncio.sleep(0.3)  # Simulate work
        
        market_data = {
            'sp500_pe_ratio': 18.5,
            'bond_yield_10y': 4.2,
            'gdp_growth': 2.5,
            'inflation': 3.1,
            'market_outlook': 'neutral',  # bullish, neutral, bearish
            'sector_valuations': {
                'tech': 'expensive',
                'healthcare': 'fair',
                'energy': 'cheap'
            }
        }
        
        await self.publish({'market': market_data})
        print(f"[{self.agent_id}] Published market data")

class RiskProfilingAgent(AsyncAgent):
    async def execute(self):
        """Wait for client data, then calculate risk profile."""
        # Wait for client data to be available
        while 'client' not in self.bus.get_context():
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(0.4)  # Simulate calculation
        
        client = self.bus.get_context().get('client', {})
        
        risk_profile = {
            'risk_score': client.get('risk_tolerance', 0.5),
            'current_allocation': {
                'equity': 0.60,
                'bonds': 0.30,
                'cash': 0.10
            },
            'recommended_allocation': {
                'equity': 0.65,
                'bonds': 0.25,
                'cash': 0.10
            },
            'portfolio_volatility': 12.3,  # Annual %
            'sharpe_ratio': 0.95
        }
        
        await self.publish({'risk_profile': risk_profile})
        print(f"[{self.agent_id}] Published risk profile")

class ProductRecommendationAgent(AsyncAgent):
    async def execute(self):
        """Wait for all input, then recommend products."""
        # Wait for context
        required = ['client', 'market', 'risk_profile']
        while not all(k in self.bus.get_context() for k in required):
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(0.5)  # Simulate recommendation
        
        context = self.bus.get_context()
        
        recommendations = {
            'top_products': [
                {
                    'product': 'Balanced Index Fund',
                    'score': 0.92,
                    'reason': 'Low cost, diversified, matches risk profile'
                },
                {
                    'product': 'Growth ETF',
                    'score': 0.85,
                    'reason': 'Higher growth for long time horizon'
                },
                {
                    'product': 'Bond Fund',
                    'score': 0.78,
                    'reason': 'Stabilizer for portfolio'
                }
            ]
        }
        
        await self.publish({'recommendations': recommendations})
        print(f"[{self.agent_id}] Published recommendations")

class ComplianceAgent(AsyncAgent):
    async def execute(self):
        """Check compliance of recommendation."""
        # Wait for recommendations
        while 'recommendations' not in self.bus.get_context():
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(0.3)  # Simulate compliance check
        
        recommendations = self.bus.get_context()['recommendations']
        
        compliance_check = {
            'compliant': True,
            'checks': {
                'fiduciary_duty': 'PASS',
                'suitability': 'PASS',
                'documentation': 'PASS',
                'disclosure': 'PASS'
            },
            'notes': 'All recommendations meet SEC/FINRA standards'
        }
        
        await self.publish({'compliance': compliance_check})
        print(f"[{self.agent_id}] Published compliance check")

# Usage
async def recommend_for_client():
    """Run all agents and collect result."""
    
    bus = ContextBus()
    
    # Create agents
    agents = [
        ClientDataAgent('client_agent', bus),
        MarketDataAgent('market_agent', bus),
        RiskProfilingAgent('risk_agent', bus),
        ProductRecommendationAgent('product_agent', bus),
        ComplianceAgent('compliance_agent', bus)
    ]
    
    # Run all concurrently
    print("[Orchestrator] Starting agent execution")
    start = time.time()
    
    await asyncio.gather(*[agent.execute() for agent in agents])
    
    elapsed = time.time() - start
    print(f"[Orchestrator] Completed in {elapsed:.2f}s")
    
    # Retrieve final recommendation
    context = bus.get_context()
    
    result = {
        'client_id': context['client']['client_id'],
        'recommendations': context['recommendations']['top_products'],
        'compliance': context['compliance']['compliant'],
        'reasoning': {
            'risk_profile': context['risk_profile'],
            'market_outlook': context['market']['market_outlook']
        }
    }
    
    return result

# Run
result = asyncio.run(recommend_for_client())
print(f"\nFinal result:\n{json.dumps(result, indent=2)}")
```

### Design Decisions & Why

**1. Why Async Parallel Execution?**
- Agents don't block each other
- Client agent and Market agent run simultaneously (independent)
- Risk agent starts once client data arrives
- Product agent starts once risk + market data arrive
- Total time: max of all paths, not sum

**2. Why Message Bus Instead of Direct Calls?**
- Agents are decoupled: don't know about each other
- Easy to add new agent (just subscribe to bus)
- Order-independent: agents publish when ready
- Testable: agents can be tested with mocked context bus

**3. Why Shared Context on Bus?**
- All agents contribute to shared understanding
- Product agent doesn't re-fetch client data (it reads from bus)
- Reduces token usage: each agent only computes its domain
- Natural data flow: agents publish, others consume

**4. Why Compliance Agent Last?**
- It needs output from Product Agent (what were recommended?)
- Compliance runs after recommendation is generated
- If compliance fails, can escalate before showing advisor

### Key Takeaways

1. **Async parallel execution is faster**: agents don't block each other. Client + Market run together.

2. **Message bus decouples agents**: agents don't know about each other, just publish/subscribe to context.

3. **Shared context reduces redundancy**: one agent fetches data, others read from bus. Saves computation.

4. **Sequential gates enforce constraints**: Compliance runs after Product, ensuring recommendation is checked.

5. **Microservices mentality scales**: with 5 agents it's simple; with 50 agents, message bus keeps you sane.
