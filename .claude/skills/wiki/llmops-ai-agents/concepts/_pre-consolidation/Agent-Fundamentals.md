---
title: Agent Fundamentals
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, foundations, agent-loop, agent-types]
confidence: high
source_files: 1
---

# Agent Fundamentals

Most people start learning about AI agents by installing a framework, importing a library, and following a quickstart. That is the wrong place to start.

Before you write a single line of agent code, you need to understand what an agent actually is, how it differs from a plain LLM call, and what architectural components every agent system is built from. This chapter gives you that foundation.

---

## An Agent Is Not a Prompt

A plain LLM call looks like this:

```python
response = llm.generate(
    prompt="Summarize this document: {document_text}"
) 
```

That is not an agent. That is a function call. It takes an input, produces an output, and it is done. There is no loop, no decision-making, no interaction with the outside world.

An agent is fundamentally different. An agent **observes its environment, reasons about what to do, takes an action, and then observes the result of that action** — in a loop. It does not just respond. It acts, watches what happens, and decides what to do next.

---

## Think About It First: A Real-World Analogy

**Imagine you are a chef in a restaurant kitchen.**

It is lunch rush. You get an order: "Make a pasta primavera." What do you do?

1. **Look around** — Do I have fresh zucchini? Is the pasta pot boiling? (PERCEIVE)
2. **Decide** — I need to chop vegetables first, then boil pasta, then sauce. (REASON)
3. **Do something** — You start chopping vegetables. (ACT)
4. **Check the result** — Zucchini is sliced. Good. But the pasta pot needs to boil for 2 more minutes. (OBSERVE)
5. **Repeat** — Next, move to the pasta. Check if it is ready. Then sauce. Then plate. (REPEAT)

You do not get the order and instantly produce the dish. You observe, decide, act, check the result, and do it again. You are in a loop.

**That is an agent.**

A plain LLM call is like asking a cookbook author to write a recipe. An agent is like actually cooking—you are in the kitchen, adapting as you go.

---

## The Agent Loop (In English First)

Here is the agent loop as a simple numbered list, before any code:

1. **Perceive** — Receive input from the environment. This could be a user message, the result of a tool you just called, or data from a database query.
2. **Reason** — Use the LLM to decide what to do next. Should you call a tool? Should you give a final answer? What information do you need?
3. **Act** — Execute the action the LLM decided on. Call a tool, query a database, send an email, write a file.
4. **Observe** — See what happened. Did the tool succeed? What data did it return? What changed in the world?
5. **Repeat** — Go back to Reason. Keep looping until the task is done or you hit a step limit.

This is the **agent loop**. Every agent you will ever build — from a simple Q&A assistant to a 50-agent enterprise system — runs this loop.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks a weather agent "What's the weather in Tokyo?"
>
> **INPUT:** "What's the weather in Tokyo?"
>
> **Step 1 (Perceive):** Agent receives the text "What's the weather in Tokyo?"
> **Step 2 (Reason):** Agent thinks: "I need weather data. I have a 'weather_tool'. Let me use it."
> **Step 3 (Act):** Agent calls `weather_tool("Tokyo")`
> **Step 4 (Observe):** Tool returns `{"temp": 22, "condition": "sunny"}`
> **Step 5 (Reason again):** "I have the data now. I can answer."
> **Step 6 (Respond):** Agent formats a final answer.
>
> **OUTPUT:** "It's 22°C and sunny in Tokyo right now."

Now let's see that loop as actual code:

## The Agent Loop In Code

```python
class SimpleAgent:
    def __init__(self, llm, tools, max_steps=10):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.memory = []

    def run(self, user_request):
        # PERCEIVE: Add the user's request to memory
        self.memory.append({"role": "user", "content": user_request})
        # REPEAT: Loop until we have a final answer or hit the step limit
        system_prompt = "your job is to generate reasoning/steps to act on give {USER REQUEST, TOOL}"
        for step in range(self.max_steps):
            # REASON: Ask the LLM what to do next
            response = self.llm.generate(
                system_prompt=self.system_prompt,
                messages=self.memory
            )
            
            # CHECK: Did the LLM decide to return a final answer?
            if response.is_final_answer:
                return response.content
            
            # ACT: Execute the tool the LLM chose
            tool_name = response.tool_call.name
            tool_args = response.tool_call.arguments
            tool_result = self.tools[tool_name].execute(**tool_args)
            
            # OBSERVE: Add the result back to memory so the LLM can see what happened
            self.memory.append({"role": "assistant", "content": response})
            self.memory.append({"role": "tool", "content": tool_result})
        
        return "Reached maximum steps without a final answer."
```

**Line-by-line breakdown:**

- `self.llm = llm` — Store the language model. This is the "brain" that makes decisions.
- `self.tools = tools` — Store the tools the agent can use. Each tool is a function like "search" or "send_email".
- `self.max_steps = max_steps` — Limit how many times the loop can run. Prevents infinite loops.
- `self.memory = []` — Start with empty memory. We will fill this with the conversation history.
- `self.memory.append({"role": "user", "content": user_request})` — Add the user's request to memory. The LLM will see this.
- `for step in range(self.max_steps):` — Start the loop. Run at most 10 times (or whatever max_steps is).
- `response = self.llm.generate(system_prompt=self.system_prompt, messages=self.memory)` — Ask the LLM: "Given the conversation history, what should we do next?" The LLM will respond with either a tool call or a final answer.
- `if response.is_final_answer:` — Check if the LLM said "I have the answer, stop looping."
- `return response.content` — If yes, return the answer and exit the function.
- `tool_name = response.tool_call.name` — Extract which tool the LLM wants to use.
- `tool_args = response.tool_call.arguments` — Extract the arguments for that tool (like a search query).
- `tool_result = self.tools[tool_name].execute(**tool_args)` — Actually run the tool. Execute it with the arguments.
- `self.memory.append({"role": "assistant", "content": response})` — Add the LLM's decision to memory.
- `self.memory.append({"role": "tool", "content": tool_result})` — Add the tool's result to memory. Next loop, the LLM will see this result and decide what to do next.

---

## Stop and Think

Before we go deeper, ask yourself: **What is the difference between a single LLM call and this loop?**

- Single call: Question in → LLM → Answer out. Done.
- Agent loop: Question in → LLM → Tool call → Tool result → back to LLM → next decision → eventually answer out.

The loop means the agent can use information it did not have in the first response. It can observe, adapt, and try again. That is what makes it an agent.

---

## The Anatomy of an Agent

Every agent, regardless of complexity, has four core components:

```
┌─────────────────────────────────────────────────┐
│                  ENVIRONMENT                     │
│                                                  │
│   ┌──────────┐    ┌───────────┐    ┌─────────┐  │
│   │ SENSORS  │───▶│ LLM BRAIN │───▶│ACTUATORS│  │
│   │          │    │           │    │         │  │
│   │ • user   │    │ • reason  │    │ • tools │  │
│   │   input  │    │ • plan    │    │ • APIs  │  │
│   │ • tool   │    │ • decide  │    │ • write │  │
│   │   results│    │           │    │ • send  │  │
│   └──────────┘    └─────┬─────┘    └─────────┘  │
│                         │                        │
│                    ┌────┴────┐                   │
│                    │ MEMORY  │                   │
│                    │         │                   │
│                    │ • chat  │                   │
│                    │   history│                  │
│                    │ • facts │                   │
│                    │ • state │                   │
│                    └─────────┘                   │
└─────────────────────────────────────────────────┘
```

### The Four Components

**Sensors** — How the agent receives information about the world. Not just the user's message. Sensors include tool results, API responses, database query results, file contents, and sensor data. Anything the agent can perceive.

**LLM Brain** — The reasoning engine. The LLM takes everything the sensors have collected, plus the agent's memory, and decides what to do next. This is where prompting, context engineering, and model selection matter. The brain decides, but cannot act by itself.

**Actuators** — How the agent changes the world. Tools, API calls, database writes, sending emails, creating files, updating records. An agent that can only read and respond is a Q&A system, not a full agent. Actuators are what make an agent an agent.

**Memory** — What the agent remembers. This can be as simple as the conversation history in the context window, or as complex as a vector database of past interactions, user preferences, and procedural knowledge.

Here is how these components map to actual code:

```python
class AgentAnatomy:
    """
    Every agent has these four components.
    The complexity varies, but the structure is always the same.
    """
    
    # ENVIRONMENT: Define what the agent can see and do
    environment = {
        "allowed_tools": ["search", "calculator", "database_query"],
        "allowed_actions": ["read", "write", "send_notification"],
        "constraints": ["never expose PII", "always cite sources"],
        "user_interface": "chat"
    }
    
    # SENSORS: How the agent receives information
    def perceive(self, user_input, tool_results=None):
        observations = {
            "user_message": user_input,
            "tool_results": tool_results or [],
            "current_time": datetime.now(),
            "session_context": self.get_session_context()
        }
        return observations
    
    # LLM BRAIN: How the agent reasons
    def reason(self, observations):
        context = self.build_context(observations)
        response = self.llm.generate(
            system_prompt=self.system_prompt,
            messages=context
        )
        return self.parse_decision(response)
    
    # ACTUATORS: How the agent acts on the world
    def act(self, decision):
        if decision.type == "tool_call":
            return self.execute_tool(decision.tool, decision.args)
        elif decision.type == "final_answer":
            return self.format_response(decision.content)
        elif decision.type == "escalate":
            return self.escalate_to_human(decision.reason)
    
    # MEMORY: What the agent remembers
    def update_memory(self, observation, decision, result):
        self.short_term_memory.append({
            "observation": observation,
            "decision": decision,
            "result": result,
            "timestamp": datetime.now()
        })
        if self.should_persist(result):
            self.long_term_memory.store(result)
```

**Line-by-line breakdown of the `perceive` method:**

- `def perceive(self, user_input, tool_results=None):` — This method takes the user's input and any results from previous tool calls.
- `"user_message": user_input,` — Store the user's message. The agent needs to know what the user asked.
- `"tool_results": tool_results or [],` — Store the results from tools the agent just called. If no tools were called, this is an empty list.
- `"current_time": datetime.now(),` — Record the current time. Some agents need to know what time it is (for tasks like "remind me at 5pm").
- `"session_context": self.get_session_context()` — Get any context about the current session, like the user's ID, their timezone, their preferences.
- `return observations` — Return all the observations as a dictionary. The brain will use these to decide what to do.

---

## The 7 Agent Types

Not all agents are the same. Different problems require different levels of sophistication. Here are the 7 agent types, ordered from simplest to most complex. Each one is a real-world metaphor first, then a simple function, then a class version.

---

### Type 1: Simple Reflex Agent

**Real-world analogy:** An email classifier. It sees the subject line and sender, instantly classifies it into a category (billing, technical, sales), and sends it to the right folder. No thinking. No memory. Pattern matching.

**When to use it:** When the task is classification or routing with a fixed set of categories.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** An email arrives at the company inbox.
>
> **INPUT:** "Hi, I was charged twice for my subscription this month. Please fix this."
>
> **Step 1:** Agent reads the email text.
> **Step 2:** Agent sends text to LLM: "Classify this as billing, technical, sales, or complaint."
> **Step 3:** LLM returns: "billing"
> **Step 4:** Agent looks up the rule: billing → finance_team@company.com
>
> **OUTPUT:** `{"category": "billing", "routed_to": "finance_team@company.com"}`
>
> That's it. No loop. No memory. One input, one output.

Now let's see how this looks in code:

#### Simple Function Version

Before we write a class, let us see the idea as a simple function:

```python
def classify_email(email_text):
    """Simple classification. One call in, one category out."""
    
    # Ask the LLM to classify
    response = llm.generate(
        prompt=f"Classify this email into: billing, technical, sales, or complaint.\n\nEmail: {email_text}"
    )
    
    category = response.strip()
    return category
```

**What this does:** Takes an email, asks the LLM to classify it, returns the category. No loop. No memory. One input, one output.

#### Class Version

Now, the same idea as a class, with tools to actually route the email:

```python
class SimpleReflexAgent:
    """
    A simple reflex agent that routes inputs based on rules.
    No memory. No planning. Just pattern matching.
    
    Example: Email router that sends emails to the right department.
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.rules = {
            "billing": "finance_team@company.com",
            "technical": "support_team@company.com",
            "sales": "sales_team@company.com",
            "complaint": "escalation_team@company.com"
        }
    
    def run(self, email_text):
        # One LLM call to classify — no loop, no memory
        category = self.llm.generate(
            prompt=f"""Classify this email into exactly one category: 
            billing, technical, sales, or complaint.
            
            Email: {email_text}
            
            Return only the category name."""
        )
        
        destination = self.rules.get(category.strip(), "general_inbox@company.com")
        return {"category": category, "routed_to": destination}
```

**Line-by-line breakdown:**

- `self.rules = {...}` — A lookup table. Each category maps to an email address. This is the "reflex" — a direct mapping from input to output.
- `self.llm.generate(prompt=...)` — Ask the LLM to classify the email. This is the only decision the agent makes.
- `destination = self.rules.get(category.strip(), ...)` — Look up the destination email for this category. If the category is not found, default to "general_inbox".
- `return {"category": category, "routed_to": destination}` — Return both the classification and where the email was routed.

**Why it is "reflex":** The agent does not think about the decision. It sees a pattern (the email content) and instantly produces an output (the category). No reasoning, no planning, no memory.

---

### Type 2: Model-Based Reflex Agent

**Real-world analogy:** A price tracker app. It checks the price of a product, compares it to the previous price it saw, and alerts you if the price dropped below your threshold. It remembers the old price, so it can reason about the change.

**When to use it:** When the agent needs to track state changes over time.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A price tracker is monitoring a laptop. The user set an alert threshold of $800.
>
> **Check 1 (yesterday):**
> **INPUT:** product="laptop_x", current_price=$899, threshold=$800
> **Step 1:** Agent checks world model → no previous price for "laptop_x"
> **Step 2:** Agent stores: `{"laptop_x": {"price": 899}}`
> **OUTPUT:** `{"action": "track", "message": "Started tracking"}`
>
> **Check 2 (today):**
> **INPUT:** product="laptop_x", current_price=$749, threshold=$800
> **Step 1:** Agent checks world model → previous price was $899
> **Step 2:** Agent compares: $749 < $800 threshold AND $899 >= $800 (it crossed!)
> **Step 3:** Agent updates world model: `{"laptop_x": {"price": 749}}`
> **OUTPUT:** `{"action": "alert", "message": "Price dropped from 899 to 749"}`
>
> The key difference: the agent REMEMBERS the old price. That memory changes its decision.

Now let's see how this looks in code:

#### Simple Function Version

```python
def track_price(product_id, current_price, price_history):
    """Remember the old price, reason about the change."""
    
    previous_price = price_history.get(product_id, None)
    
    if previous_price is None:
        return "Started tracking"
    
    if current_price < previous_price:
        return f"Price dropped from {previous_price} to {current_price}!"
    
    return "No change"
```

**What this does:** Takes the current price and the history, compares them, and returns a decision based on the change.

#### Class Version

```python
class ModelBasedReflexAgent:
    """
    Tracks the state of the world and uses it to inform decisions.
    
    Example: A price tracker that monitors product prices and alerts
    when prices drop below a threshold — but only if the price
    actually changed (not just re-checked).
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.world_model = {}  # Internal model of current state
    
    def run(self, product_id, current_price, alert_threshold):
        # PERCEIVE: Look up the previous price we tracked
        previous_price = self.world_model.get(product_id, None)
        
        # UPDATE: Update the world model with the current price
        if product_id not in self.world_model:
            self.world_model[product_id] = {
                "price": current_price,
                "last_checked": datetime.now(),
                "price_history": []
            }
        
        self.world_model[product_id]["price"] = current_price
        self.world_model[product_id]["price_history"].append(current_price)
        
        # REASON: Make decision based on the world model
        if previous_price is None:
            return {"action": "track", "message": "Started tracking"}
        
        # REASON: If price dropped below threshold, alert
        if current_price < alert_threshold and previous_price >= alert_threshold:
            return {
                "action": "alert",
                "message": f"Price dropped from {previous_price} to {current_price}",
                "change": current_price - previous_price
            }
        
        return {"action": "no_change", "price": current_price}
```

**Line-by-line breakdown:**

- `self.world_model = {}` — A dictionary that tracks what we know about the world. In this case, the prices of products.
- `previous_price = self.world_model.get(product_id, None)` — Look up what the price was last time we checked. If we have never checked this product, return None.
- `self.world_model[product_id] = {...}` — Update the world model. Record the new price, the timestamp, and the history.
- `if previous_price is None:` — If this is the first time we are tracking this product, start tracking it.
- `if current_price < alert_threshold and previous_price >= alert_threshold:` — Alert only if the price actually crossed the threshold (it was above before, now it is below).

**Key difference from simple reflex:** The agent remembers what it saw before. It knows the price was $50 last time and is $42 now, so it can reason about the change.

---

### Type 3: Goal-Based Agent

**Real-world analogy:** A trip planner. You tell it "I want to book a trip to Paris next month." It makes a plan: (1) search for flights, (2) search for hotels, (3) check the weather, (4) book everything. It executes each step, checks if it worked, and replans if needed.

**When to use it:** When the task requires multiple steps and the agent needs to figure out the right sequence.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks "Book me a trip to Paris next month for under $2000."
>
> **INPUT:** "Book a trip to Paris, budget $2000, next month"
>
> **Step 1 (Plan):** Agent asks LLM to create a plan:
>   - Task 1: Search flights to Paris for next month
>   - Task 2: Search hotels near central Paris
>   - Task 3: Check total cost stays under $2000
>   - Task 4: Book if within budget
> **Step 2 (Execute Task 1):** Calls flight_search tool → finds flight for $650
> **Step 3 (Execute Task 2):** Calls hotel_search tool → finds hotel for $900 (7 nights)
> **Step 4 (Execute Task 3):** $650 + $900 = $1,550 → under $2,000 ✓
> **Step 5 (Execute Task 4):** Books flight and hotel
>
> **What if Task 2 failed?** (No hotels available)
> **Step 3b (Replan):** Agent creates a new plan: "Search Airbnb instead of hotels"
> **Step 4b:** Calls airbnb_search tool → finds option for $700
> **Step 5b:** Books everything
>
> **OUTPUT:** "Trip booked! Flight: $650, Hotel: $900, Total: $1,550 (under your $2,000 budget)"

Now let's see how this looks in code:

#### Simple Function Version

```python
def plan_trip(goal):
    """Make a plan, then execute it step by step."""
    
    plan = llm.generate(
        prompt=f"Create a step-by-step plan to: {goal}"
    )
    
    steps = parse_plan(plan)  # Convert text to a list of steps
    
    for step in steps:
        result = execute_step(step)
        print(f"Completed: {step} -> {result}")
    
    return "Trip planned!"
```

**What this does:** Creates a plan, then executes each step in order. No replanning—just follows the original plan.

#### Class Version

```python
class GoalBasedAgent:
    """
    Plans a sequence of actions to reach a goal.
    
    Example: A trip planner that books flights, hotels, and 
    activities to match a user's travel preferences.
    """
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, goal):
        # Step 1: Create a plan
        plan = self.llm.generate(
            prompt=f"""Given this goal: {goal}
            
            Create a step-by-step plan. For each step, specify:
            - what tool to use
            - what information is needed
            - what the expected output is
            
            Return as a JSON list of steps."""
        )
        
        steps = json.loads(plan)
        results = []
        
        # Step 2: Execute each step
        for i, step in enumerate(steps):
            print(f"Executing step {i+1}/{len(steps)}: {step['description']}")
            
            tool = self.tools[step["tool"]]
            result = tool.execute(**step["arguments"])
            results.append(result)
            
            # Step 3: Check if we need to replan
            if not result.success:
                revised_plan = self.replan(goal, steps, results, i)
                steps = revised_plan
        
        # Step 4: Synthesize results
        return self.synthesize(goal, results)
    
    def replan(self, goal, original_plan, results_so_far, failed_step):
        """When a step fails, create a new plan from the current state."""
        return self.llm.generate(
            prompt=f"""The original plan was: {original_plan}
            
            Steps completed so far: {results_so_far}
            Step {failed_step + 1} failed.
            
            Create a revised plan to still achieve the goal: {goal}
            Start from the current state, not from scratch."""
        )
```

**Line-by-line breakdown:**

- `plan = self.llm.generate(prompt=f"Create a step-by-step plan...")` — Ask the LLM to decompose the goal into steps. It returns a JSON string describing each step.
- `steps = json.loads(plan)` — Convert the JSON string into a Python list of step dictionaries.
- `for i, step in enumerate(steps):` — Loop through each step in the plan.
- `tool = self.tools[step["tool"]]` — Look up the tool for this step.
- `result = tool.execute(**step["arguments"])` — Execute the tool with the arguments from the plan.
- `if not result.success:` — Check if the step succeeded. If not, replan.
- `revised_plan = self.replan(goal, steps, results, i)` — Ask the LLM to create a new plan starting from the current state.
- `steps = revised_plan` — Replace the old plan with the new plan. Keep executing from where we left off.

**Key difference from model-based:** The agent does not just track state — it actively plans how to change the state to reach a goal. It can also replan when things go wrong.

---

### Type 4: Utility-Based Agent

**Real-world analogy:** A route finder. There are 5 ways to get to work. Route A is fast but expensive. Route B is cheap but slow. Route C is scenic. You rank them by how good they are for your preferences (you care about time more than cost), and pick the best one.

**When to use it:** When there are multiple valid solutions and the agent needs to pick the best one.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks "Find me the best route to work." They care most about speed, then cost, then comfort.
>
> **INPUT:** origin="Home", destination="Office", preferences={"time_weight": 0.6, "cost_weight": 0.25, "comfort_weight": 0.15}
>
> **Step 1 (Find options):** Route finder returns 3 candidates:
>   - Route A: 25 min drive, $8 toll, comfort 4/5
>   - Route B: 40 min bus, $2.50 fare, comfort 3/5
>   - Route C: 35 min train, $3.00 fare, comfort 5/5
>
> **Step 2 (Score each route):**
>   - Route A: time=0.75 × 0.6 + cost=0.84 × 0.25 + comfort=0.80 × 0.15 = **0.78**
>   - Route B: time=0.20 × 0.6 + cost=0.95 × 0.25 + comfort=0.60 × 0.15 = **0.45**
>   - Route C: time=0.38 × 0.6 + cost=0.94 × 0.25 + comfort=1.00 × 0.15 = **0.61**
>
> **Step 3 (Pick the best):** Route A has the highest score (0.78)
>
> **OUTPUT:** `{"route": "Route A (25 min drive)", "utility": 0.78, "reason": "Best for your time-first preference"}`

Now let's see how this looks in code:

#### Simple Function Version

```python
def find_best_route(routes, preferences):
    """Score each route, pick the highest score."""
    
    best_score = -1
    best_route = None
    
    for route in routes:
        score = compute_utility(route, preferences)
        if score > best_score:
            best_score = score
            best_route = route
    
    return best_route
```

**What this does:** Scores each option and returns the one with the highest score.

#### Class Version

```python
class UtilityBasedAgent:
    """
    Evaluates multiple options and picks the one with the highest utility.
    
    Example: A route finder that balances travel time, cost, 
    number of stops, and scenic value.
    """
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, origin, destination, preferences):
        # Step 1: Generate candidate solutions
        candidates = self.tools["route_finder"].find_routes(origin, destination)
        
        # Step 2: Score each candidate on multiple dimensions
        scored = []
        for route in candidates:
            score = self.compute_utility(route, preferences)
            scored.append({"route": route, "utility": score})
        
        # Step 3: Pick the highest utility option
        best = max(scored, key=lambda x: x["utility"])
        return best
    
    def compute_utility(self, route, preferences):
        """
        Utility function: weighted combination of factors.
        The weights come from user preferences.
        """
        time_score = 1.0 - (route.duration / self.max_duration)
        cost_score = 1.0 - (route.cost / self.max_cost)
        comfort_score = route.comfort_rating / 5.0
        
        utility = (
            preferences.get("time_weight", 0.4) * time_score +
            preferences.get("cost_weight", 0.4) * cost_score +
            preferences.get("comfort_weight", 0.2) * comfort_score
        )
        return utility
```

**Line-by-line breakdown:**

- `candidates = self.tools["route_finder"].find_routes(origin, destination)` — Get all possible routes.
- `for route in candidates:` — For each route, compute a utility score.
- `score = self.compute_utility(route, preferences)` — Calculate how good this route is for the user.
- `time_score = 1.0 - (route.duration / self.max_duration)` — Convert time to a score. If the route takes half the max time, time_score = 0.5 (good).
- `cost_score = 1.0 - (route.cost / self.max_cost)` — Same for cost.
- `comfort_score = route.comfort_rating / 5.0` — Convert the comfort rating (1-5) to a 0-1 scale.
- `utility = (preferences.get("time_weight", 0.4) * time_score + ...)` — Weighted sum. If the user cares about time more, time_weight will be 0.6 instead of 0.4.
- `best = max(scored, key=lambda x: x["utility"])` — Find the route with the highest utility.

**Key difference from goal-based:** A goal-based agent asks "does this reach the goal?" A utility-based agent asks "of all the ways to reach the goal, which one is best according to my utility function?"

---

### Type 5: Learning Agent

**Real-world analogy:** A recommendation engine that learns. At first, it recommends random things. Users click on some recommendations and ignore others. The engine tracks which recommendations worked and learns to recommend similar things next time.

**When to use it:** When the agent will handle many similar tasks over time and should get better at them.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A recommendation engine is suggesting articles to a user. It has been learning from their feedback.
>
> **Request 1 (no feedback history yet):**
> **INPUT:** user_id="jane", request="Suggest an article"
> **Step 1:** Check feedback store → empty (no history)
> **Step 2:** No lessons to apply → use default recommendation
> **OUTPUT:** Recommends a long technical article → User gives thumbs DOWN 👎
> **Feedback stored:** "jane found long technical articles unhelpful"
>
> **Request 2 (has 1 feedback):**
> **INPUT:** user_id="jane", request="Suggest an article"
> **Step 1:** Check feedback store → 1 entry: "long technical articles = unhelpful"
> **Step 2:** Extract lesson: "Avoid long technical articles for this user"
> **Step 3:** Apply lesson in LLM prompt: "Based on feedback, recommend shorter, practical articles"
> **OUTPUT:** Recommends a short practical guide → User gives thumbs UP 👍
> **Feedback stored:** "jane liked short practical guides"
>
> **Request 3 (has 2 feedbacks):**
> **Step 1:** Lessons: "Avoid long technical. Prefer short practical."
> **OUTPUT:** Even better recommendation → User loves it 👍👍
>
> The agent gets smarter with every interaction.

Now let's see how this looks in code:

#### Simple Function Version

```python
def recommend_with_learning(user_id, feedback_history):
    """Learn from past feedback, apply lessons to new recommendation."""
    
    lessons = extract_lessons(feedback_history)  # What worked before?
    
    recommendation = llm.generate(
        prompt=f"Based on these lessons: {lessons}, recommend something new."
    )
    
    return recommendation
```

**What this does:** Looks at past feedback, extracts patterns, applies those patterns to the next recommendation.

#### Class Version

```python
class LearningAgent:
    """
    Learns from feedback and improves over time.
    
    Example: A recommendation engine that gets better as it 
    learns which recommendations users actually click on.
    """
    
    def __init__(self, llm, tools, feedback_store):
        self.llm = llm
        self.tools = tools
        self.feedback_store = feedback_store
    
    def run(self, user_id, context):
        # Step 1: Retrieve past feedback for this type of request
        past_feedback = self.feedback_store.get_relevant(
            user_id=user_id,
            context_type=context.type,
            limit=10
        )
        
        # Step 2: Extract lessons from past feedback
        lessons = self.extract_lessons(past_feedback)
        
        # Step 3: Ask the LLM to apply those lessons
        response = self.llm.generate(
            prompt=f"""Based on previous interactions, here are things 
            that worked well and things that did not:
            
            {lessons}
            
            Now handle this request: {context.request}
            
            Apply the lessons above to improve your response."""
        )
        
        return response
    
    def receive_feedback(self, interaction_id, feedback):
        """Called when a user gives feedback on the agent's output."""
        self.feedback_store.add({
            "interaction_id": interaction_id,
            "feedback": feedback,  # e.g., "helpful", "wrong", "too verbose"
            "timestamp": datetime.now()
        })
    
    def extract_lessons(self, feedback_list):
        """Turns raw feedback into actionable patterns."""
        if not feedback_list:
            return "No feedback yet."
        
        return self.llm.generate(
            prompt=f"""Analyze these {len(feedback_list)} past feedback items 
            and extract 3-5 actionable patterns:
            
            {json.dumps(feedback_list)}
            
            Format: what to do more of, what to avoid."""
        )
```

**Line-by-line breakdown:**

- `past_feedback = self.feedback_store.get_relevant(user_id=user_id, ...)` — Retrieve feedback from past interactions with this user.
- `lessons = self.extract_lessons(past_feedback)` — Ask the LLM to find patterns in the feedback.
- `response = self.llm.generate(prompt=f"Based on these lessons: {lessons}, ...")` — When handling a new request, include the lessons in the prompt.
- `self.feedback_store.add({...})` — Store feedback from the user about the agent's last response.

**Key difference from utility-based:** The utility function in a utility-based agent is fixed. A learning agent's behavior changes over time based on experience. It gets smarter every time a user gives it feedback.

---

### Type 6: Hierarchical Agent

**Real-world analogy:** A manager at a company. The manager gets a big project, breaks it into smaller tasks, and assigns each task to a specialist. The HR specialist handles HR work, the finance specialist handles budgeting, etc. Each specialist works on their own piece. The manager collects the results and synthesizes them into a final answer.

**When to use it:** When the task is too complex for one agent, and different parts require different expertise.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks "How much will it cost to give all employees a 5% raise, and are there any legal issues?"
>
> **INPUT:** "How much will it cost to give all employees a 5% raise, and are there any legal issues?"
>
> **Step 1 (Manager decomposes):** Manager agent breaks the request into subtasks:
>   - Subtask A → HR Agent: "Get employee count and current salary data"
>   - Subtask B → Finance Agent: "Calculate cost of 5% raise" (depends on A)
>   - Subtask C → Legal Agent: "Check legal requirements for salary changes"
>
> **Step 2 (Execute A — HR Agent):** 
>   → Returns: {"employee_count": 150, "total_payroll": "$12,000,000/year"}
>
> **Step 3 (Execute B — Finance Agent, using A's results):**
>   → Receives HR data → Calculates: $12,000,000 × 5% = $600,000/year additional
>   → Returns: {"additional_cost": "$600,000/year", "per_employee_avg": "$4,000"}
>
> **Step 4 (Execute C — Legal Agent, runs independently):**
>   → Returns: {"issues": ["Must provide 30-day written notice", "Check minimum wage compliance in all states"]}
>
> **Step 5 (Manager synthesizes):**
>   → Combines all results into one answer
>
> **OUTPUT:** "A 5% raise for 150 employees would cost $600,000/year ($4,000 avg per employee). Legal requirements: you must provide 30-day written notice and verify minimum wage compliance across all states."

Now let's see how this looks in code:

#### Simple Function Version

```python
def manage_project_with_specialists(project):
    """Break project into tasks, assign to specialists, collect results."""
    
    tasks = llm.generate(
        prompt=f"Break this project into specialist tasks: {project}"
    )
    
    results = {}
    for task in tasks:
        specialist = get_specialist(task.domain)
        result = specialist.do_work(task)
        results[task.id] = result
    
    final = synthesize(results)
    return final
```

**What this does:** Breaks work into pieces, delegates to specialists, collects results.

#### Class Version

```python
class HierarchicalAgent:
    """
    Decomposes a task and delegates to specialist sub-agents.
    
    Example: A multi-department assistant that routes HR questions 
    to an HR agent, finance questions to a finance agent, etc.
    """
    
    def __init__(self, llm, sub_agents):
        self.llm = llm
        self.sub_agents = sub_agents  # {"hr": HRAgent, "finance": FinanceAgent, ...}
    
    def run(self, user_request):
        # Step 1: Decompose the request into subtasks
        plan = self.llm.generate(
            prompt=f"""Break this request into subtasks. 
            Available specialist agents: {list(self.sub_agents.keys())}
            
            Request: {user_request}
            
            For each subtask, specify which agent should handle it
            and what information that agent needs.
            
            Return as JSON: [{{"agent": "...", "task": "...", "depends_on": []}}]"""
        )
        
        subtasks = json.loads(plan)
        results = {}
        
        # Step 2: Execute subtasks (respecting dependencies)
        for task in self.topological_sort(subtasks):
            agent = self.sub_agents[task["agent"]]
            
            # Pass results from dependency tasks to this agent
            dependency_results = {
                dep: results[dep] for dep in task.get("depends_on", [])
            }
            
            result = agent.run(task["task"], context=dependency_results)
            results[task["id"]] = result
        
        # Step 3: Synthesize all results
        return self.synthesize(user_request, results)
```

**Line-by-line breakdown:**

- `plan = self.llm.generate(prompt=f"Break this request into subtasks...")` — Ask the LLM to decompose the request.
- `subtasks = json.loads(plan)` — Convert the plan JSON into a list of subtasks.
- `for task in self.topological_sort(subtasks):` — Execute subtasks in order, respecting dependencies. If task C depends on task A and B, do A and B first.
- `agent = self.sub_agents[task["agent"]]` — Look up the specialist agent for this task.
- `dependency_results = {dep: results[dep] for dep in task.get("depends_on", [])}` — Collect the results from tasks that this task depends on.
- `result = agent.run(task["task"], context=dependency_results)` — Ask the specialist agent to do its work, passing the dependency results.
- `results[task["id"]] = result` — Store the result so other tasks can use it.

**Key difference from goal-based:** A goal-based agent executes steps itself. A hierarchical agent delegates to other agents, each with their own capabilities, tools, and context.

---

### Type 7: Multi-Agent System

**Real-world analogy:** A fraud detection team. 5 different analysts each look at the same credit card transaction from different angles: one checks the IP address, one checks the spending pattern, one checks the merchant, one checks recent travel, one checks the account history. They each come to a conclusion independently, then vote. The final decision requires agreement from the majority.

**When to use it:** When the problem requires collaboration between agents with different perspectives, or when you need redundancy and diversity.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A credit card transaction comes in. The fraud detection team (5 agents) needs to decide if it's fraud.
>
> **INPUT:** Transaction: $2,500 purchase at electronics store in Miami, cardholder lives in Seattle, 11:30 PM
>
> **Step 1 (All agents analyze independently):**
>   - IP Agent: "IP is from Miami, cardholder is in Seattle" → verdict: SUSPICIOUS
>   - Spending Agent: "User usually spends <$200, this is $2,500" → verdict: SUSPICIOUS
>   - Merchant Agent: "Electronics store is a common fraud category" → verdict: SUSPICIOUS
>   - Travel Agent: "No flights booked to Miami, no prior Miami activity" → verdict: FRAUD
>   - History Agent: "Account is 5 years old, good standing" → verdict: SAFE
>
> **Step 2 (Agents see each other's findings and can revise):**
>   - History Agent revises: "Account is good, BUT 4 other agents flagged it" → changes to SUSPICIOUS
>
> **Step 3 (Vote — majority rules):**
>   - SUSPICIOUS: 3 votes, FRAUD: 1 vote, SAFE: 0 votes → Decision: **SUSPICIOUS**
>   - Confidence: 5/5 agents agree it's not safe = high confidence
>
> **OUTPUT:** `{"decision": "flag_for_review", "confidence": 0.95, "votes": {"suspicious": 4, "fraud": 1, "safe": 0}}`

Now let's see how this looks in code:

#### Simple Function Version

```python
def detect_fraud_with_team(transaction):
    """Each analyst analyzes independently, then vote on fraud."""
    
    votes = []
    
    ip_analyst = IPAnalyzer()
    votes.append(ip_analyst.is_fraud(transaction))
    
    spending_analyst = SpendingAnalyzer()
    votes.append(spending_analyst.is_fraud(transaction))
    
    merchant_analyst = MerchantAnalyzer()
    votes.append(merchant_analyst.is_fraud(transaction))
    
    decision = "fraud" if votes.count(True) >= 2 else "safe"
    return decision
```

**What this does:** Multiple independent analysts each evaluate the transaction, then the team votes.

#### Class Version

```python
class MultiAgentSystem:
    """
    Multiple agents collaborating to solve a problem.
    
    Example: A fraud detection network where different agents 
    analyze different signals and vote on whether a transaction 
    is fraudulent.
    """
    
    def __init__(self, agents, voting_strategy="majority"):
        self.agents = agents  # List of specialist agents
        self.voting_strategy = voting_strategy
        self.message_bus = MessageBus()
    
    def run(self, transaction):
        # Step 1: All agents analyze independently
        analyses = {}
        for agent in self.agents:
            analysis = agent.analyze(transaction)
            analyses[agent.name] = analysis
            
            # Agents can publish findings for others to see
            self.message_bus.publish(
                sender=agent.name,
                topic="analysis_complete",
                data=analysis
            )
        
        # Step 2: Agents can revise based on others' findings
        for agent in self.agents:
            others_findings = self.message_bus.get_messages(
                exclude_sender=agent.name,
                topic="analysis_complete"
            )
            revised = agent.revise(transaction, others_findings)
            analyses[agent.name] = revised
        
        # Step 3: Aggregate decisions
        if self.voting_strategy == "majority":
            votes = [a["decision"] for a in analyses.values()]
            decision = max(set(votes), key=votes.count)
        elif self.voting_strategy == "unanimous":
            decision = "flag" if all(
                a["decision"] == "flag" for a in analyses.values()
            ) else "pass"
        
        return {
            "decision": decision,
            "individual_analyses": analyses,
            "confidence": self.compute_confidence(analyses)
        }
```

**Line-by-line breakdown:**

- `for agent in self.agents:` — Loop through each agent.
- `analysis = agent.analyze(transaction)` — Each agent independently analyzes the transaction.
- `self.message_bus.publish(...)` — Each agent publishes its findings so others can see.
- `for agent in self.agents:` — Second loop. Now agents can revise their analysis based on what others found.
- `others_findings = self.message_bus.get_messages(exclude_sender=agent.name, ...)` — Retrieve messages from other agents (but not this one).
- `revised = agent.revise(transaction, others_findings)` — Ask the agent to reconsider its conclusion in light of what others found.
- `decision = max(set(votes), key=votes.count)` — Find the most common decision (majority vote).

**Key difference from hierarchical:** In a hierarchical system, one agent is in charge and delegates. In a multi-agent system, agents are peers. They may have different opinions, and the system needs a strategy to resolve disagreements (voting, consensus, etc.).

---

## Stop and Think

You now know the 7 agent types. Before moving on, ask yourself:

- Which agent type would you use for a customer support bot?
- Which would you use for a data analysis assistant?
- Could you combine more than one type? How?

---

## When to Use an Agent (and When Not To)

This is one of the most important decisions you will make: **does this problem actually need an agent?**

### Use an agent when:

- The task requires multiple steps that depend on intermediate results
- The system needs to make decisions based on observations (not just generate text)
- The task involves interacting with external tools, APIs, or databases
- The system needs to handle unpredictable inputs and adapt its behavior
- There is a loop: act, observe, decide, act again

### Do NOT use an agent when:

- A single LLM call produces the right answer (summarization, classification, translation)
- The workflow is fully deterministic and can be hardcoded (no decisions to make)
- Latency matters more than flexibility (agents add overhead from multiple LLM calls)
- The task does not involve any tools or external state changes

Here is a decision framework in code:

```python
def should_use_agent(task_description):
    """
    Decision framework: does this task need an agent?
    """
    checks = {
        "multi_step": task_description.requires_multiple_steps,
        "tool_use": task_description.needs_external_tools,
        "decision_making": task_description.involves_conditional_logic,
        "observation_loop": task_description.needs_to_check_results,
        "unpredictable_input": task_description.input_varies_significantly,
    }
    
    agent_score = sum(checks.values())
    
    if agent_score >= 3:
        return "YES — use an agent"
    elif agent_score == 2:
        return "MAYBE — consider a simple agent or a chain"
    else:
        return "NO — a single LLM call or a hardcoded pipeline is enough"
```

**Practical rule of thumb:** If you can draw the solution as a single box with one input and one output, you do not need an agent. If you need a loop with arrows going back, you need an agent.

---

## In Production, This Looks Like

Here is what a real agent project folder structure looks like:

```
my-agent/
├── agent/
│   ├── __init__.py
│   ├── simple_agent.py        # Core agent loop
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search.py          # Each tool is its own file
│   │   ├── calculator.py
│   │   └── database.py
│   └── memory/
│       ├── __init__.py
│       ├── short_term.py      # Conversation history
│       └── long_term.py       # Persistent knowledge
├── config/
│   ├── __init__.py
│   ├── system_prompts.py      # Prompts live here
│   └── agent_config.yaml      # Agent settings (max_steps, etc.)
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_memory.py
├── main.py                     # Entry point
└── requirements.txt            # Dependencies
```

**Key principles:**
- Tools are in separate files. Each tool is its own module.
- Configuration (prompts, max_steps, etc.) is not hardcoded. It lives in a config file.
- Memory is abstracted. You have short-term (current conversation) and long-term (database) memory.
- Tests exist. Agent code is business logic, so it needs tests.

---

## Key Vocabulary

These terms will be used throughout the rest of the course. Make sure you can define each one before moving on.

| Term | Definition | Example |
|------|-----------|---------|
| **Agent** | A system that perceives, reasons, acts, and observes in a loop | A coding assistant that reads code, plans a fix, writes the fix, runs tests, and iterates |
| **Agent Loop** | The perceive → reason → act → observe → repeat cycle | The `for step in range(max_steps)` loop in the code above |
| **Tool** | A function the agent can call to interact with the outside world | A search API, a database query, a calculator |
| **Tool Call** | A structured request from the LLM to execute a specific tool | `{"tool": "search", "query": "latest quarterly revenue"}` |
| **Observation** | The result of a tool call or action, fed back into the agent's context | The search results returned by the search API |
| **Context Window** | The total amount of text the LLM can see at once (prompt + history + tool results) | GPT-4: ~128K tokens, Claude: ~200K tokens |
| **System Prompt** | The instructions that define the agent's identity, constraints, and behavior | "You are a financial analyst. Never recommend specific stocks." |
| **Memory** | Any state the agent maintains beyond the current context window | Conversation history, user preferences, past tool results |
| **Reasoning Trace** | The full log of what the agent thought, decided, and did at each step | Step 1: searched for X. Step 2: found Y. Step 3: concluded Z. |
| **Orchestrator** | An agent that plans and delegates work to other agents | A manager agent that assigns subtasks to specialist workers |
| **Worker Agent** | An agent that executes a specific subtask assigned by an orchestrator | A "data retrieval" agent that fetches market data |
| **Guardrail** | A filter or check that constrains the agent's inputs or outputs | A PII detector that blocks the agent from returning personal data |

---

## Developing Your AI Capability

This section is important. It is about being honest about what you can and cannot do at this stage, and how to avoid a common trap.

### What AI Can Help You With At This Stage

- **Brainstorming agent designs.** Ask an LLM: "I want to build an agent that helps with X. What agent type would you recommend and why?"
- **Explaining Python syntax.** Ask: "What does `**kwargs` mean?" or "How do classes and `self` work?"
- **Reviewing architecture sketches.** Ask an LLM to review your hand-drawn or text-based diagram of an agent architecture.
- **Debugging agent behavior.** Ask: "My agent keeps calling the search tool even after it has enough information. Why might that be?"

### What YOU Must Understand Yourself

- **The agent loop.** You need to know perceive → reason → act → observe in your bones. When you read any agent code, you should instantly recognize where in the loop it is.
- **Why each component exists.** You should understand why we need sensors, memory, a brain, and actuators. Know what breaks if you remove one.
- **When to use vs. not use an agent.** Be able to look at a problem and say "this is a multi-step looping task, we need an agent" or "this is just classification, a single LLM call is fine."
- **The 7 types and when they fit.** You do not need to memorize all 7, but you should know the difference between simple reflex (no memory), model-based (memory of state), goal-based (planning), and utility-based (optimization).

### The LLM Fallacy: A Warning

**This is critical:** If you ask an LLM to write agent code for you and just copy-paste it, you will think you understand agents — but you will not.

Here is the trap:

1. You ask ChatGPT: "Write me a simple agent."
2. It returns beautiful, working code.
3. You run it. It works! It actually works!
4. You feel smart. You think you understand agents.
5. Later, when it breaks or behaves unexpectedly, you have no idea why. You are lost.

**The problem:** The output looked smart, so you think the understanding is yours. But you just watched a magic trick. You do not know how it works.

**The fix:** Always trace through every line of code yourself. Ask:

- "Where is the perceive step? Where is the reason step?"
- "What would happen if I removed this line?"
- "Why did the author choose this data structure instead of another?"
- "If the LLM calls a tool that does not exist, what happens?"

Do this for every code block in this chapter. If you cannot answer those questions, ask an LLM to explain the line, then read the explanation. Do not move on until you can explain it back.

### Exercises: Practice Your Understanding

Try these exercises. Use AI to help, but verify your understanding.

**Exercise 1: Identify the agent type**

Read the code for the LearningAgent above. Now, without looking, write down:
- What is the environment it operates in?
- What are its sensors? (What information does it perceive?)
- What is its actuator? (What action does it take?)
- What does it remember? (What is in its memory?)

Now check your answers against the code. Did you get it right?

**Exercise 2: Trace the loop**

Look at the GoalBasedAgent code. Trace through the full agent loop:
- Perceive: Where does user input come in?
- Reason: Where does the LLM decide what to do?
- Act: Where does the agent execute a tool?
- Observe: Where does the agent see the result?
- Repeat: Where does the loop happen?

Draw a diagram. Label each part.

**Exercise 3: Decision-making**

You are building a system. Here are 5 tasks. For each, decide: does it need an agent? If yes, which type(s)?

1. Summarize a 20-page document into a 1-page outline.
2. Monitor a server and send an alert if CPU usage exceeds 80%.
3. Plan a wedding (find venue, book caterer, arrange flowers, send invitations).
4. Translate a sentence from English to Spanish.
5. Write a product recommendation based on a user's purchase history.

For each one, write a 1-sentence explanation of your choice. Then ask an LLM to review your answers.

---

## What You Should Be Able to Do Now

After reading this chapter, you should be able to:

1. Explain the difference between a plain LLM call and an agent
2. Draw the agent loop (perceive → reason → act → observe → repeat)
3. Name and describe the 4 components of every agent (sensors, LLM brain, actuators, memory)
4. Describe all 7 agent types and give an example of when each is appropriate
5. Decide whether a given problem requires an agent or a simpler solution
6. Identify the 4 components in a real agent codebase
7. Avoid the LLM Fallacy by tracing code and understanding every line

---

Next: [Agentic Design Patterns →](./02-agentic-design-patterns.md)
