---
title: Multi-Agent Orchestration
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, foundations, orchestration, multi-agent, coordination]
confidence: high
source_files: 1
---

# Multi-Agent Orchestration

A single agent can handle a lot. But when the task gets large enough — multiple data sources, different expertise required, parallel workloads, or enterprise-scale complexity — you need multiple agents working together.

This chapter teaches you the 5 orchestration patterns that govern how multi-agent systems are structured. Every multi-agent system you will encounter is a variation of one of these five.

---

## Why Multiple Agents?

A single agent has limits:

- **Context window:** One agent cannot hold all the knowledge for all domains simultaneously
- **Specialization:** A single prompt cannot make an agent expert at finance AND legal AND engineering
- **Parallelism:** One agent processes one thing at a time
- **Isolation:** When one capability fails, you want it to fail without breaking everything else
- **Testability:** Smaller, focused agents are easier to test and evaluate than one monolithic agent

The question is not "should I use multiple agents?" but "how should they coordinate?"

---

## The 5 Orchestration Patterns

```
1. Orchestrator-Worker     →  One boss, many specialists
2. Sequential Pipeline     →  Assembly line
3. Parallel Fan-Out/In     →  Divide and conquer
4. Hierarchical            →  Org chart
5. Event-Driven / Reactive →  Independent responders
```

---

## Pattern 1: Orchestrator-Worker

### The Analogy First

Think about how a restaurant kitchen works. The **head chef** (orchestrator) receives an order from the front-of-house. Instead of doing everything themselves, they:

1. Break it down: "We need the patties grilled, toppings prepped, and fries cooked"
2. Delegate: "Grill station, handle the patties. Prep station, do the toppings. Fryer, start the fries"
3. Track progress: "Are we ready? Not yet? Good, keep going"
4. Synthesize: Once everything is ready, assemble the final burger and send it out

Each specialist (worker) only knows their job. The head chef coordinates everything. That's Orchestrator-Worker.

### Why It Works

- **Specialization:** Each worker gets really good at one thing
- **Scalability:** You can add more workers without changing the orchestrator's logic much
- **Failure isolation:** If the fryer breaks, the grill station keeps working
- **Debuggable:** You can test each worker independently

### Stop and Think

Before we code, ask yourself: "If I had to ask three different experts to help me with a task, what specific thing would I ask each one to do?" Write that down. That's your worker decomposition.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks "Analyze this customer complaint email."
>
> **INPUT:** "I've been waiting 3 weeks for my refund. Your service is terrible. I want to speak to a manager."
>
> **Step 1 (Orchestrator receives the request):** Reads the email.
> **Step 2 (Orchestrator creates a plan):** "I need: sentiment analysis, category detection, and a draft response."
>   - Subtask 1 → Sentiment Worker: "Analyze the emotional tone"
>   - Subtask 2 → Category Worker: "What department handles this?"
>   - Subtask 3 → Response Writer: "Draft a reply" (depends on subtasks 1 and 2)
>
> **Step 3 (Dispatch to Sentiment Worker):**
>   → Worker analyzes the text
>   → Returns: `{"sentiment": "angry", "score": 0.85}`
>
> **Step 4 (Dispatch to Category Worker):**
>   → Worker classifies the complaint
>   → Returns: `{"category": "billing", "subcategory": "refund_delay"}`
>
> **Step 5 (Dispatch to Response Writer — receives results from steps 3 & 4):**
>   → Knows the customer is angry about a billing/refund issue
>   → Returns: `{"draft": "Dear valued customer, I sincerely apologize for the delay with your refund. I've escalated this to our billing team and you should receive your refund within 48 hours..."}`
>
> **Step 6 (Orchestrator synthesizes):** Combines all worker results.
>
> **OUTPUT:**
> ```
> {
>   "sentiment": "angry (0.85)",
>   "category": "billing/refund_delay",
>   "suggested_response": "Dear valued customer, I sincerely apologize...",
>   "priority": "high"
> }
> ```

Now let's see how this looks in code — starting with the simplest version:

---

## Pattern 1 Implementation: Simple Version First

Let's start with the simplest possible version — just plain functions, no classes.

```python
# --- SIMPLEST VERSION: Plain functions ---

def worker_fetch_data(task_description):
    """A worker that fetches data from an API."""
    print(f"[Worker: Data Fetcher] Running: {task_description}")
    # Simulate fetching data
    return {"stocks": ["AAPL", "MSFT", "TSLA"], "fetched_at": "2024-10-15"}

def worker_analyze(task_description, data_from_previous_worker):
    """A worker that analyzes the data."""
    print(f"[Worker: Analyzer] Running: {task_description}")
    print(f"[Worker: Analyzer] Received data: {data_from_previous_worker}")
    # Simulate analysis
    return {"analysis": "AAPL is trending up", "confidence": 0.85}

def orchestrator_simple(user_request):
    """The simplest orchestrator: just run workers in sequence."""
    print(f"\n[Orchestrator] Received request: {user_request}\n")
    
    # Step 1: Call first worker
    data_result = worker_fetch_data("Get stock data for top 3 tech stocks")
    
    # Step 2: Call second worker, pass the result from step 1
    analysis_result = worker_analyze("Analyze the stock trends", data_result)
    
    # Step 3: Synthesize
    final_answer = f"Based on the data and analysis: {analysis_result['analysis']}"
    
    return final_answer

# --- USE IT ---
answer = orchestrator_simple("What should I invest in?")
print(f"\nFinal Answer: {answer}")
```

**Line-by-line explanation:**

1. `def worker_fetch_data(task_description):` → We're defining a function called `worker_fetch_data` that takes one input
2. `print(f"[Worker: Data Fetcher] Running: {task_description}")` → Print what this worker is doing (for debugging)
3. `return {"stocks": [...]}` → Return a dictionary (a structured result) so the next step knows what we got
4. `def worker_analyze(task_description, data_from_previous_worker):` → This worker takes TWO inputs: the task AND the result from the previous worker
5. `print(f"[Worker: Analyzer] Received data: {data_from_previous_worker}")` → Show what data we received (debugging)
6. `def orchestrator_simple(user_request):` → The orchestrator function that coordinates everything
7. `data_result = worker_fetch_data(...)` → Call worker 1, store its result
8. `analysis_result = worker_analyze(..., data_result)` → Call worker 2, pass the result from worker 1
9. `final_answer = f"Based on the data and analysis: ..."` → Combine everything into a final answer

**Output when you run this:**
```
[Orchestrator] Received request: What should I invest in?

[Worker: Data Fetcher] Running: Get stock data for top 3 tech stocks
[Worker: Analyzer] Running: Analyze the stock trends
[Worker: Analyzer] Received data: {'stocks': ['AAPL', 'MSFT', 'TSLA'], 'fetched_at': '2024-10-15'}

Final Answer: Based on the data and analysis: AAPL is trending up
```

---

### Pattern 1 Implementation: Class Version

Now let's make it more robust with classes. This is the "production-ready" version.

> **What is a class?** Think of a class as a template for creating a worker that remembers its configuration. Instead of passing the LLM every time, we create a Worker object once, and it keeps the LLM "inside" itself. We access it with `self.llm`.

```python
class OrchestratorWorkerSystem:
    """
    One orchestrator decomposes the task and delegates to specialist workers.
    
    This is the most common multi-agent pattern. Use it when:
    - The task naturally breaks into specialist subtasks
    - Different workers need different tools or knowledge
    - You want to test and iterate on workers independently
    """
    
    def __init__(self, orchestrator_llm, workers):
        self.orchestrator_llm = orchestrator_llm
        self.workers = workers  # {"data": DataWorker, "analysis": AnalysisWorker, ...}
    
    def run(self, user_request):
        # --- STEP 1: PLAN ---
        plan = self.orchestrator_llm.generate(
            system_prompt="""You are an orchestrator. Your job is to break down 
            the user's request into subtasks and assign each to the right worker.
            
            Available workers:
            - data_retrieval: Fetches data from databases and APIs
            - news_analysis: Reads and summarizes news articles
            - financial_modeling: Runs calculations and projections
            - risk_assessment: Evaluates risks and uncertainties
            - report_writer: Produces formatted reports
            
            Return a JSON plan:
            [
                {
                    "id": "step_1",
                    "worker": "data_retrieval",
                    "task": "Fetch Q3 2024 revenue for TSMC",
                    "depends_on": []
                },
                ...
            ]""",
            messages=[{"role": "user", "content": user_request}]
        )
        
        subtasks = json.loads(plan)
        results = {}
        
        # --- STEP 2: EXECUTE (respecting dependencies) ---
        execution_order = self.topological_sort(subtasks)
        
        for task in execution_order:
            worker = self.workers[task["worker"]]
            
            # Build context from completed dependencies
            dependency_context = {
                dep_id: results[dep_id] 
                for dep_id in task.get("depends_on", [])
                if dep_id in results
            }
            
            # Execute the worker
            print(f"[{task['id']}] → {task['worker']}: {task['task']}")
            result = worker.run(
                task=task["task"],
                context=dependency_context
            )
            results[task["id"]] = result
            
            # Check for failure
            if result.get("status") == "failed":
                recovery = self.handle_failure(task, result, results)
                if recovery:
                    results[task["id"]] = recovery
                else:
                    print(f"[{task['id']}] FAILED — skipping dependent tasks")
        
        # --- STEP 3: SYNTHESIZE ---
        final_answer = self.orchestrator_llm.generate(
            prompt=f"""The user asked: {user_request}
            
            Here are the results from all workers:
            {json.dumps(results, indent=2)}
            
            Synthesize these into a coherent, complete response.
            If any worker failed, note what information is missing."""
        )
        
        return {
            "answer": final_answer,
            "plan": subtasks,
            "worker_results": results
        }
    
    def handle_failure(self, failed_task, error, completed_results):
        """
        When a worker fails, the orchestrator decides what to do:
        1. Retry with a modified task
        2. Use a different worker
        3. Skip and note the gap
        4. Escalate to human
        """
        decision = self.orchestrator_llm.generate(
            prompt=f"""Worker '{failed_task["worker"]}' failed on task: 
            {failed_task["task"]}
            
            Error: {error}
            
            Options:
            1. RETRY — try the same task with different parameters
            2. ALTERNATIVE — use a different worker
            3. SKIP — proceed without this result
            4. ESCALATE — ask a human for help
            
            What should we do?"""
        )
        return self.execute_recovery(decision, failed_task)
    
    def topological_sort(self, tasks):
        """Sort tasks so dependencies are executed first."""
        visited = set()
        order = []
        task_map = {t["id"]: t for t in tasks}
        
        def visit(task_id):
            if task_id in visited:
                return
            visited.add(task_id)
            for dep in task_map[task_id].get("depends_on", []):
                visit(dep)
            order.append(task_map[task_id])
        
        for task in tasks:
            visit(task["id"])
        
        return order
```

**Line-by-line explanation (key parts):**

1. `class OrchestratorWorkerSystem:` → We're creating a class (a template for creating orchestrator objects)
2. `def __init__(self, orchestrator_llm, workers):` → The `__init__` method (pronounced "dunder init") runs when you create a new OrchestratorWorkerSystem. The `self` keyword means "this specific instance"
3. `self.orchestrator_llm = orchestrator_llm` → Store the LLM inside `self` so we can use it later with `self.orchestrator_llm.generate(...)`
4. `self.workers = workers` → Store the workers dictionary inside `self`
5. `def run(self, user_request):` → The method that actually runs the orchestration. Again, `self` means "use the LLM and workers I stored earlier"
6. `subtasks = json.loads(plan)` → Convert the LLM's JSON response into a Python dictionary (structure we can work with)
7. `for task in execution_order:` → Loop through each task in the correct order
8. `worker = self.workers[task["worker"]]` → Get the right worker from our workers dictionary using the task's worker name
9. `result = worker.run(...)` → Call that worker and store what it returns

---

### A Complete Walkthrough Example

Let's walk through ONE complete request end-to-end:

**User asks:** "What should I invest in? I care about tech companies with low risk."

**Step 1: Orchestrator creates a plan**

The orchestrator's LLM generates:
```json
[
  {
    "id": "step_1",
    "worker": "data_retrieval",
    "task": "Get financial data for Apple, Microsoft, Google, Meta",
    "depends_on": []
  },
  {
    "id": "step_2",
    "worker": "risk_assessment",
    "task": "Evaluate volatility and risk metrics for the stocks from step_1",
    "depends_on": ["step_1"]
  },
  {
    "id": "step_3",
    "worker": "financial_modeling",
    "task": "Project 5-year growth for low-risk stocks from step_2",
    "depends_on": ["step_2"]
  },
  {
    "id": "step_4",
    "worker": "report_writer",
    "task": "Create final investment recommendation based on steps 1-3",
    "depends_on": ["step_3"]
  }
]
```

**Step 2: Orchestrator executes workers in order**

- `step_1` runs (no dependencies): Data Retrieval Worker fetches prices, P/E ratios, dividend yields
- `step_2` runs (depends on step_1): Risk Assessment Worker calculates volatility, beta, drawdown risk
- `step_3` runs (depends on step_2): Financial Modeling Worker projects growth for low-volatility stocks only
- `step_4` runs (depends on step_3): Report Writer creates the final investment recommendation

**Step 3: Orchestrator synthesizes**

Takes all the worker results and asks the LLM: "Synthesize all this into one clear recommendation for the user"

**Result:** "Based on the analysis, I recommend Microsoft and Apple. Both are in tech, have low volatility (acceptable risk), and strong 5-year growth projections."

---

### Worker Contract

Every worker should follow a standard interface so the orchestrator knows what to expect:

```python
class BaseWorker:
    """
    Standard interface for all workers.
    
    Every worker:
    1. Accepts a task description and optional context
    2. Returns a structured result with status, data, and metadata
    3. Handles its own errors and returns clean error messages
    4. Never crashes the orchestrator
    """
    
    def run(self, task, context=None):
        try:
            result = self.execute(task, context)
            return {
                "status": "success",
                "data": result,
                "worker": self.name,
                "execution_time": self.timer.elapsed(),
                "tokens_used": self.token_counter.total()
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "worker": self.name,
                "can_retry": self.is_retryable(e)
            }
```

**Why this contract matters:** The orchestrator doesn't need to know HOW each worker does its job. It just expects to call `worker.run(task, context)` and get back a dictionary with "status", "data", and metadata. This makes it easy to swap workers in and out.

---

## Pattern 2: Sequential Pipeline

### The Analogy First

Think about an assembly line at a car factory:
- **Station 1** → Weld the chassis
- **Station 2** → Install the engine (uses the welded chassis from Station 1)
- **Station 3** → Install the transmission (uses the engine-equipped chassis)
- **Station 4** → Paint (uses the assembled car)
- **Station 5** → Quality check and ship

Each station receives the output of the previous station. The car transforms at each step. That's a Sequential Pipeline.

### Stop and Think

Think of a task you do regularly that has clear sequential steps. Write them down. (Example: "Write an email" → "Review spelling" → "Add attachments" → "Send". That's sequential.)

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** An invoice arrives as raw text and needs to be processed through 4 stages.
>
> **INPUT:** "Invoice from Acme Corp dated 2024-10-15 for $5,000.00 — consulting services rendered"
>
> **Stage 1 → Ingest:**
>   - Receives raw text (87 characters)
>   - Output: `{"raw_text": "Invoice from Acme Corp...", "chars": 87}`
>   - Passes to Stage 2 ➡️
>
> **Stage 2 → Extract:**
>   - Receives data from Stage 1
>   - Pulls out structured fields
>   - Output: adds `{"extracted": {"company_name": "Acme Corp", "invoice_date": "2024-10-15", "total_amount": 5000.00}}`
>   - Passes to Stage 3 ➡️
>
> **Stage 3 → Validate:**
>   - Receives data from Stage 2
>   - Checks: Is the amount positive? → Yes ✓
>   - Checks: Is the date valid? → Yes ✓
>   - Output: adds `{"validation_status": "valid"}`
>   - Passes to Stage 4 ➡️
>
> **Stage 4 → Format Output:**
>   - Receives validated data from Stage 3
>   - Creates clean final output
>   - Output: `{"company": "Acme Corp", "invoice_date": "2024-10-15", "amount": 5000.00, "status": "valid"}`
>
> **FINAL OUTPUT:**
> ```
> {"company": "Acme Corp", "invoice_date": "2024-10-15", "amount": 5000.00, "status": "valid"}
> ```
>
> Each stage transforms the data and passes it forward — like an assembly line. If Stage 3 had failed validation, the pipeline would have stopped and returned an error.

Now let's see how this looks in code:

---

### Pattern 2 Implementation: Simple Version First

```python
# --- SIMPLEST VERSION: Plain functions ---

def stage_1_ingest(raw_text):
    """First stage: Accept raw text."""
    print("[Stage 1: Ingest] Received raw text")
    return {"raw_text": raw_text, "chars": len(raw_text)}

def stage_2_extract(data):
    """Second stage: Extract structured fields."""
    print("[Stage 2: Extract] Pulling out names, dates, amounts...")
    # Simulate extraction
    extracted = {
        "company_name": "Acme Corp",
        "invoice_date": "2024-10-15",
        "total_amount": 5000.00
    }
    data["extracted"] = extracted
    return data

def stage_3_validate(data):
    """Third stage: Check that extracted data makes sense."""
    print("[Stage 3: Validate] Checking consistency...")
    if data["extracted"]["total_amount"] > 0:
        data["validation_status"] = "valid"
    else:
        data["validation_status"] = "invalid"
    return data

def stage_4_output(data):
    """Fourth stage: Format for final output."""
    print("[Stage 4: Output] Formatting for delivery...")
    final = {
        "company": data["extracted"]["company_name"],
        "invoice_date": data["extracted"]["invoice_date"],
        "amount": data["extracted"]["total_amount"],
        "status": data["validation_status"]
    }
    return final

def pipeline_simple(raw_text):
    """Run all stages in sequence."""
    print(f"\n[Pipeline] Starting with: {len(raw_text)} characters\n")
    
    result = stage_1_ingest(raw_text)
    result = stage_2_extract(result)
    result = stage_3_validate(result)
    result = stage_4_output(result)
    
    return result

# --- USE IT ---
output = pipeline_simple("Invoice from Acme Corp dated 2024-10-15 for $5000.00")
print(f"\nFinal Output: {output}")
```

**Line-by-line explanation:**

1. `def stage_1_ingest(raw_text):` → Define the first stage function
2. `return {"raw_text": raw_text, "chars": len(raw_text)}` → Return a dictionary (we're passing data forward)
3. `def stage_2_extract(data):` → The second stage takes the output of stage 1 as input
4. `data["extracted"] = extracted` → We ADD to the data dictionary (we don't throw away old data)
5. `return data` → Return the enriched data to the next stage
6. In `pipeline_simple()`, each line does: `result = stage_N(result)` → Take the output from the previous stage and feed it as input to the next stage

---

### Pattern 2 Implementation: Class Version

```python
class SequentialPipeline:
    """
    Each stage transforms data and passes it to the next.
    
    Use when:
    - Processing has a natural sequence (parse → extract → validate → output)
    - Each stage has a clear input/output contract
    - You want to debug by inspecting intermediate states
    """
    
    def __init__(self, stages):
        self.stages = stages  # Ordered list of stage agents
    
    def run(self, initial_input):
        current_data = initial_input
        trace = []  # Full execution log
        
        for i, stage in enumerate(self.stages):
            stage_name = stage.name
            print(f"[Stage {i+1}/{len(self.stages)}] {stage_name}")
            
            # Validate input for this stage
            if not stage.validate_input(current_data):
                return {
                    "status": "failed",
                    "failed_at": stage_name,
                    "reason": "Input validation failed",
                    "trace": trace
                }
            
            # Execute the stage
            try:
                result = stage.process(current_data)
            except Exception as e:
                # SHORT-CIRCUIT: Decide whether to continue or abort
                if stage.is_critical:
                    return {
                        "status": "failed",
                        "failed_at": stage_name,
                        "error": str(e),
                        "trace": trace
                    }
                else:
                    # Non-critical stage — use fallback and continue
                    result = stage.fallback(current_data)
            
            # Log the intermediate state
            trace.append({
                "stage": stage_name,
                "input_size": len(str(current_data)),
                "output_size": len(str(result)),
                "status": "success"
            })
            
            # Pass output to next stage
            current_data = result
        
        return {
            "status": "success",
            "result": current_data,
            "trace": trace
        }
```

**Line-by-line explanation:**

1. `def __init__(self, stages):` → Constructor takes an ordered list of stages
2. `self.stages = stages` → Store the stages inside `self` for later use
3. `for i, stage in enumerate(self.stages):` → Loop through each stage. `enumerate` gives us the index (`i`) and the stage object
4. `stage_name = stage.name` → Get the name of the current stage (like "Extract" or "Validate")
5. `if not stage.validate_input(current_data):` → Check if the data coming in is in the right format
6. `result = stage.process(current_data)` → Call the stage's process method to transform the data
7. `trace.append({...})` → Record what happened (for debugging later)
8. `current_data = result` → The output becomes the input for the next stage

---

### Key Principle: Save Intermediate State

Always save the state between stages so you can:
- Resume a failed pipeline from the last successful stage
- Debug by inspecting what each stage produced
- Re-run individual stages

```python
class PersistentPipeline(SequentialPipeline):
    """Pipeline that saves state after each stage."""
    
    def __init__(self, stages, state_store):
        super().__init__(stages)
        self.state_store = state_store
    
    def run(self, initial_input, job_id):
        # Check if we can resume from a previous run
        last_checkpoint = self.state_store.get_latest(job_id)
        
        if last_checkpoint:
            start_stage = last_checkpoint["completed_stage"] + 1
            current_data = last_checkpoint["data"]
            print(f"Resuming from stage {start_stage}")
        else:
            start_stage = 0
            current_data = initial_input
        
        for i in range(start_stage, len(self.stages)):
            stage = self.stages[i]
            current_data = stage.process(current_data)
            
            # Save checkpoint
            self.state_store.save({
                "job_id": job_id,
                "completed_stage": i,
                "data": current_data,
                "timestamp": datetime.now()
            })
        
        return current_data
```

---

## Pattern 3: Parallel Fan-Out / Fan-In

### The Analogy First

Imagine you want reviews for a restaurant. Instead of asking one food critic, you hire three:
- **Critic 1** evaluates the food quality
- **Critic 2** evaluates the service speed
- **Critic 3** evaluates the ambiance

All three review the **same restaurant** simultaneously (in parallel). Then you **merge** their reviews into one unified rating.

That's Fan-Out (spawn multiple agents on the same input) and Fan-In (merge results back together).

### Stop and Think

What's a decision you need to make where multiple perspectives would help? (Example: "Is this job offer good?" — one friend evaluates salary, another evaluates work-life balance, another evaluates growth opportunity.)

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A document needs to be reviewed before publication. Three specialist agents each check a different aspect — all at the same time.
>
> **INPUT:** Document text: "Our product is the best in the market. Studies show 95% customer satisfaction."
>
> **Step 1 (Fan-Out — all 3 agents start simultaneously):**
>
> 🔀 **Agent 1 (Fact Checker)** — starts now
> 🔀 **Agent 2 (Tone Analyzer)** — starts now
> 🔀 **Agent 3 (Policy Checker)** — starts now
>
> **Step 2 (All 3 agents work in parallel):**
>
> Agent 1 finishes (1.2s): `{"findings": ["Claim '95% satisfaction' has no cited source"]}`
> Agent 2 finishes (0.8s): `{"findings": "Professional but slightly biased toward own product"}`
> Agent 3 finishes (0.6s): `{"findings": "Complies with company policy section 3.2"}`
>
> **Step 3 (Fan-In — Merger combines all results):**
>   - Fact check: 1 unverified claim
>   - Tone: slight bias detected
>   - Policy: compliant
>   - Decision: APPROVED WITH CAUTION
>
> **OUTPUT:**
> ```
> {
>   "fact_check": ["Claim '95% satisfaction' has no cited source"],
>   "tone_check": "Professional but slightly biased",
>   "policy_check": "Compliant",
>   "overall_decision": "APPROVED with caution — add source for satisfaction claim"
> }
> ```
>
> Total time: ~1.2 seconds (the slowest agent). If we ran them sequentially, it would have taken 2.6 seconds.

Now let's see how this looks in code:

---

### Pattern 3 Implementation: Simple Version

```python
# --- SIMPLEST VERSION: Sequential but clear ---
# (Real parallel version requires async, which we'll show next)

def agent_check_facts(document):
    """Agent 1: Verify the facts in the document."""
    print("[Agent 1: Fact Checker] Verifying claims...")
    facts = ["Claim 1 is accurate", "Claim 2 has no source"]
    return {"agent": "fact_checker", "findings": facts}

def agent_check_tone(document):
    """Agent 2: Evaluate the tone and bias."""
    print("[Agent 2: Tone Analyzer] Checking tone...")
    tone = "Professional but slightly biased toward product A"
    return {"agent": "tone_analyzer", "findings": tone}

def agent_check_policy(document):
    """Agent 3: Check against company policy."""
    print("[Agent 3: Policy Checker] Comparing to policy...")
    policy_check = "Complies with policy section 3.2"
    return {"agent": "policy_checker", "findings": policy_check}

def merger_simple(results):
    """Combine all agent results into one decision."""
    print("\n[Merger] Combining results...\n")
    combined = {
        "fact_check": results[0]["findings"],
        "tone_check": results[1]["findings"],
        "policy_check": results[2]["findings"],
        "overall_decision": "APPROVED with caution"
    }
    return combined

def fan_out_fan_in_simple(document):
    """Run three agents, then merge."""
    print(f"[Pipeline] Checking document: {document}\n")
    
    # Fan-out: Launch all agents
    result1 = agent_check_facts(document)
    result2 = agent_check_tone(document)
    result3 = agent_check_policy(document)
    
    # Fan-in: Merge results
    final = merger_simple([result1, result2, result3])
    
    return final

# --- USE IT ---
output = fan_out_fan_in_simple("Our product is the best in the market")
print(f"\nFinal Decision: {output['overall_decision']}")
```

**The idea:** Run three agents on the same input. Collect their results. Merge them.

---

### Pattern 3 Implementation: Class Version (Parallel)

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor


class ParallelFanOutFanIn:
    """
    Run multiple agents in parallel, then merge their results.
    
    Use when:
    - Subtasks are INDEPENDENT (no dependencies between them)
    - Time matters (parallel = faster than sequential)
    - You need multiple perspectives on the same input
    """
    
    def __init__(self, agents, merger, timeout_seconds=30):
        self.agents = agents
        self.merger = merger
        self.timeout = timeout_seconds
    
    async def run(self, input_data):
        # --- FAN-OUT: Launch all agents simultaneously ---
        tasks = []
        for agent in self.agents:
            task = asyncio.create_task(
                self.run_with_timeout(agent, input_data)
            )
            tasks.append(task)
        
        # Wait for all to complete (or timeout)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # --- HANDLE PARTIAL FAILURES ---
        successful = {}
        failed = {}
        
        for agent, result in zip(self.agents, results):
            if isinstance(result, Exception):
                failed[agent.name] = str(result)
                print(f"[FAILED] {agent.name}: {result}")
            else:
                successful[agent.name] = result
                print(f"[OK] {agent.name}")
        
        # --- FAN-IN: Merge results ---
        merged = self.merger.merge(
            input_data=input_data,
            results=successful,
            failures=failed
        )
        
        return {
            "merged_result": merged,
            "agents_succeeded": list(successful.keys()),
            "agents_failed": list(failed.keys()),
        }
    
    async def run_with_timeout(self, agent, input_data):
        """Run an agent with a timeout. If it takes too long, cancel it."""
        try:
            return await asyncio.wait_for(
                agent.run_async(input_data),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            raise TimeoutError(f"{agent.name} timed out after {self.timeout}s")
```

**Line-by-line explanation:**

1. `async def run(self, input_data):` → An `async` function (handles parallelism)
2. `for agent in self.agents:` → Loop through each agent
3. `task = asyncio.create_task(self.run_with_timeout(agent, input_data))` → Create a task (start the agent running in the background)
4. `tasks.append(task)` → Add it to the list of tasks
5. `results = await asyncio.gather(*tasks, return_exceptions=True)` → Wait for ALL tasks to finish. The `*tasks` unpacks the list. `return_exceptions=True` means if one agent fails, keep waiting for the others
6. `for agent, result in zip(self.agents, results):` → Pair up each agent with its result
7. `if isinstance(result, Exception):` → Check if this result is an error
8. `self.merger.merge(...)` → Call the merger to combine all results

---

### Merger Strategies

Different ways to combine multiple agent outputs:

```python
class MajorityVoteMerger:
    """When agents vote on a decision, use majority rules."""
    
    def merge(self, input_data, results, failures):
        decisions = [r["decision"] for r in results.values()]
        majority = max(set(decisions), key=decisions.count)
        agreement = decisions.count(majority) / len(decisions)
        
        return {
            "decision": majority,
            "agreement_ratio": agreement,
            "individual_votes": {name: r["decision"] for name, r in results.items()},
            "note": f"{len(failures)} agents failed" if failures else None
        }


class ConfidenceWeightedMerger:
    """Weight each agent's result by its confidence score."""
    
    def merge(self, input_data, results, failures):
        weighted_scores = {}
        
        for name, result in results.items():
            for key, value in result.get("scores", {}).items():
                if key not in weighted_scores:
                    weighted_scores[key] = []
                weighted_scores[key].append({
                    "value": value,
                    "confidence": result.get("confidence", 0.5),
                    "source": name
                })
        
        # Compute weighted average for each score
        final_scores = {}
        for key, entries in weighted_scores.items():
            total_weight = sum(e["confidence"] for e in entries)
            final_scores[key] = sum(
                e["value"] * e["confidence"] / total_weight 
                for e in entries
            )
        
        return {"scores": final_scores}


class LLMSynthesisMerger:
    """Use an LLM to intelligently merge diverse agent outputs."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def merge(self, input_data, results, failures):
        synthesis = self.llm.generate(
            prompt=f"""Multiple agents analyzed this input and produced 
            different results. Synthesize them into one coherent answer.
            
            Original input: {input_data}
            
            Agent results:
            {json.dumps(results, indent=2)}
            
            Failed agents (their perspective is missing):
            {json.dumps(failures, indent=2)}
            
            Instructions:
            1. Identify points of agreement across agents
            2. Highlight any contradictions and explain which agent is more likely correct
            3. Note any gaps from failed agents
            4. Produce a single unified answer"""
        )
        return synthesis
```

---

## Pattern 4: Hierarchical (Agents of Agents)

### The Analogy First

Imagine a restaurant chain:
- **CEO** receives overall business goals: "Increase revenue by 10%"
- CEO delegates to **Regional Managers** (one for each region): "Hit 10% growth in your region"
- Each Regional Manager delegates to **Store Managers**: "Hit 10% growth in your store"
- Each Store Manager has **Line Cooks** reporting to them

There are multiple layers of orchestrators, each managing their own workers. That's Hierarchical.

### Stop and Think

Think of an organization you know (company, school, government). How many layers of management are there? Each layer has orchestrators and workers. That's what hierarchical systems look like.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A pharmaceutical company asks "Can we launch Drug X in Europe next quarter?"
>
> **INPUT:** "Can we launch Drug X in Europe next quarter?"
>
> **Step 1 (Top-Level CEO Agent):** Identifies which domains are needed:
>   - Clinical domain: "Is the drug clinically ready?"
>   - Regulatory domain: "Do we have EU approval?"
>   - Supply Chain domain: "Can we manufacture and distribute?"
>
> **Step 2 (Clinical Domain Manager runs its own workers):**
>   → Clinical Data Worker: Checks trial results → "Phase 3 complete, efficacy confirmed"
>   → Safety Worker: Checks adverse events → "2 minor side effects, within acceptable range"
>   → Clinical Manager synthesizes: `{"status": "clinically_ready", "confidence": "high"}`
>
> **Step 3 (Regulatory Domain Manager runs its own workers):**
>   → EU Compliance Worker: Checks EMA status → "Application submitted, pending review"
>   → Timeline Worker: Estimates approval → "Expected approval: 8 weeks"
>   → Regulatory Manager synthesizes: `{"status": "pending_approval", "estimated_weeks": 8}`
>
> **Step 4 (Supply Chain Domain Manager runs its own workers):**
>   → Manufacturing Worker: Checks capacity → "Can produce 1M units/month"
>   → Distribution Worker: Checks EU logistics → "Distribution network ready"
>   → Supply Manager synthesizes: `{"status": "ready", "capacity": "1M units/month"}`
>
> **Step 5 (CEO Agent synthesizes all domains):**
>
> **OUTPUT:** "Drug X launch in Europe next quarter: CONDITIONAL GO. Clinical readiness confirmed. Manufacturing ready. However, EU regulatory approval is expected in 8 weeks, which is tight for next quarter. Recommendation: prepare for launch but plan for possible 2-week delay."
>
> Key insight: The CEO Agent never talked to individual workers. Each Domain Manager handled its own team.

Now let's see how this looks in code:

---

### Pattern 4 Implementation

```python
class HierarchicalSystem:
    """
    Multi-tier agent system with domain separation.
    
    Use when:
    - The organization has clear domain boundaries
    - Different domains need different security/access levels
    - The system is too large for a single orchestrator
    - You need to add new domains without modifying existing ones
    """
    
    def __init__(self, top_level_llm, domain_managers):
        self.top_llm = top_level_llm
        self.domain_managers = domain_managers
        # {"clinical": ClinicalManager, "regulatory": RegulatoryManager, ...}
    
    def run(self, request):
        # Top-level: Identify which domains are needed
        routing = self.top_llm.generate(
            prompt=f"""Analyze this request and determine which domains 
            need to be involved.
            
            Available domains: {list(self.domain_managers.keys())}
            
            Request: {request}
            
            Return JSON:
            {{
                "domains": ["domain1", "domain2"],
                "domain_tasks": {{
                    "domain1": "specific task for domain1",
                    "domain2": "specific task for domain2"
                }},
                "cross_domain_dependencies": [
                    {{"from": "domain1", "to": "domain2", "what": "needs X from domain1"}}
                ]
            }}"""
        )
        
        routing = json.loads(routing)
        domain_results = {}
        
        # Execute domains (respecting cross-domain dependencies)
        for domain_name in self.resolve_execution_order(routing):
            manager = self.domain_managers[domain_name]
            task = routing["domain_tasks"][domain_name]
            
            # Pass any cross-domain context
            cross_domain_context = {
                dep["from"]: domain_results.get(dep["from"])
                for dep in routing.get("cross_domain_dependencies", [])
                if dep["to"] == domain_name and dep["from"] in domain_results
            }
            
            result = manager.run(task, cross_domain_context)
            domain_results[domain_name] = result
        
        # Top-level synthesis
        return self.top_llm.generate(
            prompt=f"""Synthesize results from all domains into a 
            unified response.
            
            Original request: {request}
            Domain results: {json.dumps(domain_results, indent=2)}"""
        )


class DomainManager:
    """
    A mid-level orchestrator that manages workers within one domain.
    Operates independently — the top-level doesn't know about 
    individual workers.
    """
    
    def __init__(self, domain_name, llm, workers, knowledge_base):
        self.domain_name = domain_name
        self.llm = llm
        self.workers = workers
        self.knowledge_base = knowledge_base
    
    def run(self, task, cross_domain_context=None):
        # Retrieve domain-specific knowledge
        relevant_docs = self.knowledge_base.retrieve(task)
        
        # Plan within this domain
        plan = self.llm.generate(
            prompt=f"""You manage the {self.domain_name} domain.
            
            Task: {task}
            Relevant knowledge: {relevant_docs}
            Context from other domains: {cross_domain_context}
            
            Available workers: {[w.name for w in self.workers]}
            
            Create a plan to complete this task using your workers."""
        )
        
        # Execute workers
        results = {}
        for step in json.loads(plan):
            worker = self.find_worker(step["worker"])
            results[step["id"]] = worker.run(step["task"])
        
        return self.synthesize(task, results)
```

**Key insight:** Each DomainManager is itself an orchestrator. It has its own LLM, its own workers, and its own knowledge base. The top-level doesn't micromanage the domains. It just says "Clinical domain, handle the patient intake" and the Clinical Manager figures out which workers to use.

---

### Security Boundaries in Hierarchical Systems

```python
class SecureDomainManager(DomainManager):
    """
    A domain manager with security boundaries.
    
    Critical for: healthcare (HIPAA), finance (SOX), 
    multi-tenant systems (data isolation).
    """
    
    def __init__(self, domain_name, llm, workers, knowledge_base, access_policy):
        super().__init__(domain_name, llm, workers, knowledge_base)
        self.access_policy = access_policy
    
    def run(self, task, cross_domain_context=None):
        # FILTER: Remove any data this domain shouldn't see
        safe_context = self.access_policy.filter_incoming(
            data=cross_domain_context,
            target_domain=self.domain_name
        )
        
        result = super().run(task, safe_context)
        
        # FILTER: Remove any data this domain shouldn't share
        safe_result = self.access_policy.filter_outgoing(
            data=result,
            source_domain=self.domain_name
        )
        
        return safe_result
```

**The idea:** If the Finance domain tries to receive data from the Healthcare domain, the security policy blocks it. If a Healthcare domain tries to send patient data to the Marketing domain, it gets redacted.

---

## Pattern 5: Event-Driven / Reactive

### The Analogy First

Imagine a fire alarm system in a building:
- The **fire alarm** goes off (an event)
- A **router** hears it and knows which agents should respond
- The **Firefighter Agent** immediately evacuates people
- The **Building Manager Agent** shuts down the elevator
- The **Alert System Agent** sends notifications to fire department
- Everyone reacts independently based on the event type

There's no central orchestrator saying "Firefighter, evacuate. Manager, stop elevators." Everyone just reacts to the event.

### Stop and Think

What's something that happens in your life where multiple things respond independently to a trigger? (Email arrives → your filter flags it, your phone notifies you, your email client plays a sound. All independent.)

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A new user signs up on your platform. This triggers an event that multiple agents respond to independently.
>
> **INPUT (Event):** `{"type": "user_signed_up", "data": {"email": "jane@example.com", "plan": "free", "source": "google_ads"}}`
>
> **Step 1 (Event arrives at the Event Bus):**
> The system checks: "Who is registered to handle 'user_signed_up' events?"
> → 4 agents are registered.
>
> **Step 2 (All 4 agents react independently — no one waits for anyone):**
>
> 🔔 **Welcome Agent** hears "user_signed_up":
>   → Sends welcome email to jane@example.com
>   → Result: "Email sent"
>
> 🔔 **CRM Agent** hears "user_signed_up":
>   → Creates new contact record in the database
>   → Result: "Contact created: jane@example.com"
>
> 🔔 **Analytics Agent** hears "user_signed_up":
>   → Logs the signup, updates daily counter, records ad source
>   → Result: "Signup #847 today, source: google_ads"
>
> 🔔 **Onboarding Agent** hears "user_signed_up" + plan="free":
>   → Schedules free-tier onboarding sequence (emails on day 1, 3, 7)
>   → Result: "Onboarding scheduled: 3 emails over 7 days"
>
> **What if the CRM Agent crashes?**
> → The other 3 agents keep running normally. They don't even know the CRM Agent failed.
> → The system logs the error for debugging.
>
> **OUTPUT:** 4 independent actions completed from 1 event. No orchestrator needed.

Now let's see how this looks in code:

---

### Pattern 5 Implementation

```python
class EventDrivenSystem:
    """
    Agents react to events independently.
    
    Use when:
    - Work is triggered by external events (webhooks, queues, cron)
    - Agents don't need to coordinate with each other
    - You want to add new event handlers without modifying existing ones
    - The system must handle bursty, unpredictable workloads
    """
    
    def __init__(self):
        self.handlers = {}  # event_type → list of handler agents
        self.event_queue = asyncio.Queue()
    
    def register(self, event_type, agent):
        """Register an agent to handle a specific event type."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(agent)
    
    async def process_events(self):
        """Main event loop — runs continuously."""
        while True:
            event = await self.event_queue.get()
            
            handlers = self.handlers.get(event.type, [])
            
            if not handlers:
                print(f"No handler for event type: {event.type}")
                continue
            
            # Run all handlers for this event type
            for handler in handlers:
                asyncio.create_task(
                    self.safe_handle(handler, event)
                )
    
    async def safe_handle(self, handler, event):
        """Run a handler with error isolation."""
        try:
            result = await handler.handle(event)
            await self.log_result(event, handler, result)
        except Exception as e:
            await self.log_error(event, handler, e)
            # One handler failing does NOT affect others
```

**Line-by-line explanation:**

1. `def register(self, event_type, agent):` → Register an agent to listen for a specific event type (like "alert_fired" or "user_message_sent")
2. `if event_type not in self.handlers:` → Check if we already have handlers for this event type
3. `self.handlers[event_type].append(agent)` → Add this agent to the list of handlers for this event type
4. `async def process_events(self):` → The main event loop that runs forever
5. `event = await self.event_queue.get()` → Wait for an event to arrive
6. `handlers = self.handlers.get(event.type, [])` → Get all agents registered for this event type
7. `for handler in handlers:` → For each handler, launch it
8. `asyncio.create_task(self.safe_handle(handler, event))` → Run it in the background without waiting
9. `async def safe_handle(self, handler, event):` → Wrap the handler in try/except so if it crashes, other handlers still run

---

### Example: Monitoring System

```python
class AlertAgent:
    """Handles infrastructure alerts."""
    
    async def handle(self, event):
        alert = event.data
        
        # Classify severity
        severity = self.classify(alert)
        
        if severity == "critical":
            # Immediate: page the on-call engineer
            await self.page_oncall(alert)
            return {"action": "paged", "severity": "critical"}
        
        elif severity == "warning":
            # Investigate: check if this is a known issue
            known = await self.check_known_issues(alert)
            if known:
                return {"action": "auto_resolved", "known_issue": known.id}
            else:
                await self.create_ticket(alert)
                return {"action": "ticket_created"}
        
        else:
            # Low severity: log and move on
            return {"action": "logged", "severity": "low"}
```

When an alert event fires, this agent runs independently. If there are 10 other agents registered for alerts, they all run in parallel without waiting for each other.

---

## Coordination: The 5 Questions Every Multi-Agent Architecture Must Answer

Regardless of which pattern you choose, you must answer these five critical questions. Write them down in your design document.

```python
class ArchitectureDecisions:
    """
    Every multi-agent system must answer these 5 questions.
    Document them explicitly in your design.
    """
    
    # 1. WHO MAKES THE PLAN?
    planning_strategy = "llm_based"  # Options: "llm_based", "rule_based", "hybrid"
    # llm_based: An LLM decides how to decompose the task (flexible, but unpredictable)
    # rule_based: A hardcoded router maps input types to agents (predictable, but rigid)
    # hybrid: Rules handle common cases, LLM handles edge cases (best of both)
    
    # 2. HOW DO AGENTS SHARE STATE?
    state_sharing = "message_passing"  # Options: "shared_memory", "message_passing", "database"
    # shared_memory: All agents read/write from a shared context (simple, but risky)
    # message_passing: Agents send structured messages (clean, but more boilerplate)
    # database: Agents read/write to a shared database (durable, but slower)
    
    # 3. WHAT HAPPENS WHEN A WORKER FAILS?
    failure_strategy = "retry_then_skip"  # Options: "retry", "fallback", "skip", "escalate"
    max_retries = 2
    
    # 4. WHERE IS THE HUMAN IN THE LOOP?
    human_checkpoints = ["before_action", "on_low_confidence", "on_exception"]
    # before_action: Human approves before any external action
    # after_action: Human reviews after the fact
    # on_low_confidence: Only when the agent is unsure
    # on_exception: Only when something goes wrong
    # never: Fully autonomous (use with extreme caution)
    
    # 5. HOW DO YOU OBSERVE WHAT'S HAPPENING?
    observability = {
        "traces": True,       # Full execution logs per request
        "spans": True,        # Individual step timings
        "dashboards": True,   # Real-time system health
        "cost_tracking": True # Token usage per agent
    }
```

---

## Pattern Selection Guide

Use this decision tree to pick the right pattern for your system:

```python
def choose_orchestration_pattern(requirements):
    """Which pattern fits your system?"""
    
    if requirements.is_event_triggered:
        return "EVENT_DRIVEN"
    
    elif requirements.has_domain_separation:
        if requirements.domains_need_security_isolation:
            return "HIERARCHICAL"
        else:
            return "ORCHESTRATOR_WORKER"  # with domain-specific workers
    
    elif requirements.has_clear_subtask_boundaries:
        if requirements.subtasks_are_independent:
            return "PARALLEL_FAN_OUT_FAN_IN"
        elif requirements.subtasks_are_sequential:
            return "SEQUENTIAL_PIPELINE"
        else:
            return "ORCHESTRATOR_WORKER"
    
    elif requirements.is_enterprise_scale:
        return "HIERARCHICAL"
    
    else:
        return "ORCHESTRATOR_WORKER"  # Safe default
```

---

## In Production, This Looks Like...

Real multi-agent projects structure code like this:

```
my_ai_project/
├── agents/
│   ├── orchestrator.py          # Orchestrator class
│   ├── workers/
│   │   ├── data_worker.py
│   │   ├── analysis_worker.py
│   │   └── report_worker.py
│   ├── base_worker.py           # Worker contract/interface
│   └── __init__.py
├── patterns/
│   ├── orchestrator_worker.py   # Pattern implementation
│   ├── sequential_pipeline.py
│   ├── parallel_fanout.py
│   ├── hierarchical.py
│   └── event_driven.py
├── tests/
│   ├── test_orchestrator.py     # Test orchestrator in isolation
│   ├── test_workers.py          # Test each worker independently
│   └── test_integration.py      # Test the full system
└── main.py                      # Entry point
```

Each worker lives in its own file. Each pattern has its own implementation file. Tests are separate. This makes it easy to:
- Swap workers without touching the orchestrator
- Test workers independently
- Understand which pattern you're using

---

## Developing Your AI Capability

At this stage, AI can help you:
- **Decompose complex tasks** into subtasks (give AI the user request, ask it to break it down)
- **Design worker contracts** (give AI the subtasks, ask it to write the expected input/output for each worker)
- **Draft orchestrator prompts** (AI can write the prompt that tells the orchestrator how to plan and route)
- **Generate worker scaffolds** (AI can write skeleton code for new workers)

But **YOU must understand:**
- When one agent is enough vs when you need multiple (this is an architectural choice, not a technical detail)
- How state flows between agents (message passing vs shared memory has different tradeoffs)
- What happens when a worker fails (retry? escalate? skip? This affects reliability)
- How to test each agent independently before combining them

### The LLM Fallacy

Here's the trap: You ask AI to build your multi-agent system. It writes code that looks good, runs without errors, and produces answers. You think you've built a multi-agent system.

Then at 2am, a worker hangs. The orchestrator keeps running, eating tokens, getting stuck. You have no visibility into what went wrong. You realize you don't actually understand the architecture — the AI wrote it, you just ran it.

**The check:** Can you draw the architecture for your own multi-agent system on paper WITHOUT AI help? If not, understand it first before going into production.

---

## Exercises

### Exercise 1: Design an Orchestrator-Worker System

Pick a real task from your work or life. (Examples: "Book a flight", "Write a product launch email", "Analyze a customer complaint")

Write out:
1. What's the main task?
2. What are the natural subtasks? (What would you ask different experts to do?)
3. For each subtask, what are the inputs and outputs?
4. How will the orchestrator know when to move to the next task?

Don't code yet. Just write it out on paper. This is the hard part.

### Exercise 2: Trace a Pipeline

Think of a real process with sequential steps. (Examples: "Customer order → Processing → Shipping → Delivery", "Video editing → Rendering → Upload → Publishing")

Draw the stages on paper. For each stage, write:
1. What does this stage receive from the previous stage?
2. What does it output for the next stage?
3. What can go wrong at this stage?
4. If this stage fails, can we skip it or must we retry?

### Exercise 3: Plan a Fan-Out System

Think of a decision where you'd want multiple perspectives. (Examples: "Is this candidate good for the job?", "Should we launch this product?")

Write:
1. What are the different perspectives you'd want?
2. What would each perspective evaluate?
3. How would you merge their answers into one decision?

---

## What You Should Be Able to Do Now

After reading this chapter, you should be able to:

1. Name and describe all 5 orchestration patterns
2. Implement a basic orchestrator-worker system with dependency resolution
3. Build a sequential pipeline with checkpoint persistence
4. Design a parallel fan-out/fan-in system with merge strategies
5. Know when to add hierarchy (and when it is overkill)
6. Answer the 5 coordination questions for any multi-agent design
7. Choose the right pattern for a given problem

Next: [LLMOps Essentials →](./04-llmops-essentials.md)
