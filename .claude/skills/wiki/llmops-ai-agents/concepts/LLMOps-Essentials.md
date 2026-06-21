---
title: LLMOps Essentials
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
confidence: high
consolidated_from: 6 pages
---

# LLMOps Essentials

> Consolidated from 6 related concept pages.

---

## 4 Layer LLMOps Stack A production architecture with four mandatory layers Contex

## Core Principle

LLMOps is the discipline of keeping LLM agents reliable and cost-efficient in production, structured as four mandatory layers: Context Engineering, Memory Architecture, Evaluation, and Observability & Guardrails. Every layer has specific implementation patterns — token budget allocation, memory type selection, golden dataset regression testing, and trace-span instrumentation — and skipping any layer creates a production liability. The non-negotiable principle is that developers must define correctness criteria for their domain before writing evals; AI tooling can implement but never substitute for that definitional work.

## Key Heuristics

These are the load-bearing rules for this concept.

> What is not in the context does not exist for the agent.

> More context is not always better — irrelevant context dilutes the signal and increases cost.

> LLMs pay more attention to the beginning and end of the context (primacy and recency effects). Put the most important information first and last.

> Skip any of these [4 layers], and your car becomes a liability.

> Can you write down on paper what 'correct' means for your system WITHOUT AI help? If not, you don't understand the problem yet.

> AI can help you implement evals, but YOU have to define what good looks like.

> Run evals every time you change the system.

> 10 requests/second × $0.01/request × 24 hours = $8,640/day. This happens to real companies.

## Anti-Patterns & Fixes

- Naive Context Stuffing: Concatenating all available context without token budgeting causes context window overflow, irrelevant signal dilution, and wasted cost. Fix: Use a ContextBuilder with explicit percentage budgets per component type and relevance-sorted truncation.
- Skipping Evals: Deploying without a golden dataset or defined correctness criteria means regressions and edge-case failures are discovered by users, not tests. Fix: Define what 'correct' means before deployment and run automated evals on every system change.
- AI-Generated Evals Without Human Ownership: Letting an LLM generate test cases without the developer understanding what is being tested produces a 90%-passing eval suite that misses real failure modes. Fix: The developer must define correctness criteria manually before using AI to expand test coverage.
- Amnesiac Agent (No Memory Architecture): Without persistent memory, every session starts from zero, making agents unable to reference prior interactions or user context. Fix: Implement all four memory types (in-context, episodic, semantic, procedural) appropriate to the use case.
- Unmonitored Production: Running agents without traces, cost tracking, or guardrails means failures are invisible until they cause user harm or budget overruns. Fix: Instrument every pipeline stage with spans, set cost budgets with hard stops, and attach input/output guardrail checks.

## When To Apply

Load this page when:

- Use this when building an agent that will make repeated LLM calls in production and you need to control token spend per request.
- Use this when a user's conversation history plus retrieved documents together risk exceeding the model's context window.
- Use this when an agent needs to reference information from previous sessions or remember user-specific facts across conversations.
- Use this when a production agent returns wrong, hallucinated, or out-of-scope outputs and you need to detect and block them automatically.
- Use this when you need to diagnose why an agent is slow and must isolate whether the bottleneck is retrieval, LLM latency, or guardrail processing.
- Use this when preparing to deploy an agent and you need to define a regression test suite that runs on every code or prompt change.
- Use this when costs are scaling unexpectedly and you need to route cheaper models for low-complexity queries.
- Use this when an agent handles sensitive user data and you must redact PII before it enters or exits the LLM.

## Concrete Examples

- Password reset query for 'Jane' (premium user): A 16,000-token budget is allocated across system prompt (200 tokens), user profile (50 tokens), retrieved docs (800 tokens), and conversation history (10 most recent messages), demonstrating context prioritization and budget arithmetic.
- ContextBuilder class with fit_docs and fit_history methods: Shows relevance-sorted doc inclusion with truncation fallback and recency-first history pruning in Python code.
- ContextCompressor with summarize_old_messages: Replaces old messages with a 3-5 bullet LLM-generated summary while keeping the N most recent messages verbatim.
- Full integrated agent run() method: Wires all 4 layers together — input guardrails, memory retrieval, context building, cost check, LLM generation, output guardrails, and memory storage — each wrapped in a named trace span.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**LLMOps Essentials**

An LLM coding agent generating agent infrastructure faces a specific failure mode: it will produce syntactically correct, plausible-looking eval suites and context builders without any grounding in what 'correct' actually means for the target domain, creating false confidence. The agent also cannot self-monitor costs or latency — without instrumented spans and budget checks baked into generated code, it will silently generate runaway-cost or slow pipelines with no observable signal. Critically, an LLM agent must treat context budget management as a first-class code constraint, not an afterthought, because it is itself subject to the same context window limits it is building around.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Context Budget Model A token allocation framework that assigns fixed percentage

## Core Principle

LLMOps is the discipline of keeping LLM agents reliable and cost-efficient in production, structured as four mandatory layers: Context Engineering, Memory Architecture, Evaluation, and Observability & Guardrails. Every layer has specific implementation patterns — token budget allocation, memory type selection, golden dataset regression testing, and trace-span instrumentation — and skipping any layer creates a production liability. The non-negotiable principle is that developers must define correctness criteria for their domain before writing evals; AI tooling can implement but never substitute for that definitional work.

## Key Heuristics

These are the load-bearing rules for this concept.

> What is not in the context does not exist for the agent.

> More context is not always better — irrelevant context dilutes the signal and increases cost.

> LLMs pay more attention to the beginning and end of the context (primacy and recency effects). Put the most important information first and last.

> Skip any of these [4 layers], and your car becomes a liability.

> Can you write down on paper what 'correct' means for your system WITHOUT AI help? If not, you don't understand the problem yet.

> AI can help you implement evals, but YOU have to define what good looks like.

> Run evals every time you change the system.

> 10 requests/second × $0.01/request × 24 hours = $8,640/day. This happens to real companies.

## Anti-Patterns & Fixes

- Naive Context Stuffing: Concatenating all available context without token budgeting causes context window overflow, irrelevant signal dilution, and wasted cost. Fix: Use a ContextBuilder with explicit percentage budgets per component type and relevance-sorted truncation.
- Skipping Evals: Deploying without a golden dataset or defined correctness criteria means regressions and edge-case failures are discovered by users, not tests. Fix: Define what 'correct' means before deployment and run automated evals on every system change.
- AI-Generated Evals Without Human Ownership: Letting an LLM generate test cases without the developer understanding what is being tested produces a 90%-passing eval suite that misses real failure modes. Fix: The developer must define correctness criteria manually before using AI to expand test coverage.
- Amnesiac Agent (No Memory Architecture): Without persistent memory, every session starts from zero, making agents unable to reference prior interactions or user context. Fix: Implement all four memory types (in-context, episodic, semantic, procedural) appropriate to the use case.
- Unmonitored Production: Running agents without traces, cost tracking, or guardrails means failures are invisible until they cause user harm or budget overruns. Fix: Instrument every pipeline stage with spans, set cost budgets with hard stops, and attach input/output guardrail checks.

## When To Apply

Load this page when:

- Use this when building an agent that will make repeated LLM calls in production and you need to control token spend per request.
- Use this when a user's conversation history plus retrieved documents together risk exceeding the model's context window.
- Use this when an agent needs to reference information from previous sessions or remember user-specific facts across conversations.
- Use this when a production agent returns wrong, hallucinated, or out-of-scope outputs and you need to detect and block them automatically.
- Use this when you need to diagnose why an agent is slow and must isolate whether the bottleneck is retrieval, LLM latency, or guardrail processing.
- Use this when preparing to deploy an agent and you need to define a regression test suite that runs on every code or prompt change.
- Use this when costs are scaling unexpectedly and you need to route cheaper models for low-complexity queries.
- Use this when an agent handles sensitive user data and you must redact PII before it enters or exits the LLM.

## Concrete Examples

- Password reset query for 'Jane' (premium user): A 16,000-token budget is allocated across system prompt (200 tokens), user profile (50 tokens), retrieved docs (800 tokens), and conversation history (10 most recent messages), demonstrating context prioritization and budget arithmetic.
- ContextBuilder class with fit_docs and fit_history methods: Shows relevance-sorted doc inclusion with truncation fallback and recency-first history pruning in Python code.
- ContextCompressor with summarize_old_messages: Replaces old messages with a 3-5 bullet LLM-generated summary while keeping the N most recent messages verbatim.
- Full integrated agent run() method: Wires all 4 layers together — input guardrails, memory retrieval, context building, cost check, LLM generation, output guardrails, and memory storage — each wrapped in a named trace span.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**LLMOps Essentials**

An LLM coding agent generating agent infrastructure faces a specific failure mode: it will produce syntactically correct, plausible-looking eval suites and context builders without any grounding in what 'correct' actually means for the target domain, creating false confidence. The agent also cannot self-monitor costs or latency — without instrumented spans and budget checks baked into generated code, it will silently generate runaway-cost or slow pipelines with no observable signal. Critically, an LLM agent must treat context budget management as a first-class code constraint, not an afterthought, because it is itself subject to the same context window limits it is building around.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Golden Dataset Regression Testing A curated set of verified inputoutput pairs ru

## Core Principle

LLMOps is the discipline of keeping LLM agents reliable and cost-efficient in production, structured as four mandatory layers: Context Engineering, Memory Architecture, Evaluation, and Observability & Guardrails. Every layer has specific implementation patterns — token budget allocation, memory type selection, golden dataset regression testing, and trace-span instrumentation — and skipping any layer creates a production liability. The non-negotiable principle is that developers must define correctness criteria for their domain before writing evals; AI tooling can implement but never substitute for that definitional work.

## Key Heuristics

These are the load-bearing rules for this concept.

> What is not in the context does not exist for the agent.

> More context is not always better — irrelevant context dilutes the signal and increases cost.

> LLMs pay more attention to the beginning and end of the context (primacy and recency effects). Put the most important information first and last.

> Skip any of these [4 layers], and your car becomes a liability.

> Can you write down on paper what 'correct' means for your system WITHOUT AI help? If not, you don't understand the problem yet.

> AI can help you implement evals, but YOU have to define what good looks like.

> Run evals every time you change the system.

> 10 requests/second × $0.01/request × 24 hours = $8,640/day. This happens to real companies.

## Anti-Patterns & Fixes

- Naive Context Stuffing: Concatenating all available context without token budgeting causes context window overflow, irrelevant signal dilution, and wasted cost. Fix: Use a ContextBuilder with explicit percentage budgets per component type and relevance-sorted truncation.
- Skipping Evals: Deploying without a golden dataset or defined correctness criteria means regressions and edge-case failures are discovered by users, not tests. Fix: Define what 'correct' means before deployment and run automated evals on every system change.
- AI-Generated Evals Without Human Ownership: Letting an LLM generate test cases without the developer understanding what is being tested produces a 90%-passing eval suite that misses real failure modes. Fix: The developer must define correctness criteria manually before using AI to expand test coverage.
- Amnesiac Agent (No Memory Architecture): Without persistent memory, every session starts from zero, making agents unable to reference prior interactions or user context. Fix: Implement all four memory types (in-context, episodic, semantic, procedural) appropriate to the use case.
- Unmonitored Production: Running agents without traces, cost tracking, or guardrails means failures are invisible until they cause user harm or budget overruns. Fix: Instrument every pipeline stage with spans, set cost budgets with hard stops, and attach input/output guardrail checks.

## When To Apply

Load this page when:

- Use this when building an agent that will make repeated LLM calls in production and you need to control token spend per request.
- Use this when a user's conversation history plus retrieved documents together risk exceeding the model's context window.
- Use this when an agent needs to reference information from previous sessions or remember user-specific facts across conversations.
- Use this when a production agent returns wrong, hallucinated, or out-of-scope outputs and you need to detect and block them automatically.
- Use this when you need to diagnose why an agent is slow and must isolate whether the bottleneck is retrieval, LLM latency, or guardrail processing.
- Use this when preparing to deploy an agent and you need to define a regression test suite that runs on every code or prompt change.
- Use this when costs are scaling unexpectedly and you need to route cheaper models for low-complexity queries.
- Use this when an agent handles sensitive user data and you must redact PII before it enters or exits the LLM.

## Concrete Examples

- Password reset query for 'Jane' (premium user): A 16,000-token budget is allocated across system prompt (200 tokens), user profile (50 tokens), retrieved docs (800 tokens), and conversation history (10 most recent messages), demonstrating context prioritization and budget arithmetic.
- ContextBuilder class with fit_docs and fit_history methods: Shows relevance-sorted doc inclusion with truncation fallback and recency-first history pruning in Python code.
- ContextCompressor with summarize_old_messages: Replaces old messages with a 3-5 bullet LLM-generated summary while keeping the N most recent messages verbatim.
- Full integrated agent run() method: Wires all 4 layers together — input guardrails, memory retrieval, context building, cost check, LLM generation, output guardrails, and memory storage — each wrapped in a named trace span.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**LLMOps Essentials**

An LLM coding agent generating agent infrastructure faces a specific failure mode: it will produce syntactically correct, plausible-looking eval suites and context builders without any grounding in what 'correct' actually means for the target domain, creating false confidence. The agent also cannot self-monitor costs or latency — without instrumented spans and budget checks baked into generated code, it will silently generate runaway-cost or slow pipelines with no observable signal. Critically, an LLM agent must treat context budget management as a first-class code constraint, not an afterthought, because it is itself subject to the same context window limits it is building around.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## LLM as Judge Evaluation Using a separate LLM call to score agent outputs against

## Core Principle

LLMOps is the discipline of keeping LLM agents reliable and cost-efficient in production, structured as four mandatory layers: Context Engineering, Memory Architecture, Evaluation, and Observability & Guardrails. Every layer has specific implementation patterns — token budget allocation, memory type selection, golden dataset regression testing, and trace-span instrumentation — and skipping any layer creates a production liability. The non-negotiable principle is that developers must define correctness criteria for their domain before writing evals; AI tooling can implement but never substitute for that definitional work.

## Key Heuristics

These are the load-bearing rules for this concept.

> What is not in the context does not exist for the agent.

> More context is not always better — irrelevant context dilutes the signal and increases cost.

> LLMs pay more attention to the beginning and end of the context (primacy and recency effects). Put the most important information first and last.

> Skip any of these [4 layers], and your car becomes a liability.

> Can you write down on paper what 'correct' means for your system WITHOUT AI help? If not, you don't understand the problem yet.

> AI can help you implement evals, but YOU have to define what good looks like.

> Run evals every time you change the system.

> 10 requests/second × $0.01/request × 24 hours = $8,640/day. This happens to real companies.

## Anti-Patterns & Fixes

- Naive Context Stuffing: Concatenating all available context without token budgeting causes context window overflow, irrelevant signal dilution, and wasted cost. Fix: Use a ContextBuilder with explicit percentage budgets per component type and relevance-sorted truncation.
- Skipping Evals: Deploying without a golden dataset or defined correctness criteria means regressions and edge-case failures are discovered by users, not tests. Fix: Define what 'correct' means before deployment and run automated evals on every system change.
- AI-Generated Evals Without Human Ownership: Letting an LLM generate test cases without the developer understanding what is being tested produces a 90%-passing eval suite that misses real failure modes. Fix: The developer must define correctness criteria manually before using AI to expand test coverage.
- Amnesiac Agent (No Memory Architecture): Without persistent memory, every session starts from zero, making agents unable to reference prior interactions or user context. Fix: Implement all four memory types (in-context, episodic, semantic, procedural) appropriate to the use case.
- Unmonitored Production: Running agents without traces, cost tracking, or guardrails means failures are invisible until they cause user harm or budget overruns. Fix: Instrument every pipeline stage with spans, set cost budgets with hard stops, and attach input/output guardrail checks.

## When To Apply

Load this page when:

- Use this when building an agent that will make repeated LLM calls in production and you need to control token spend per request.
- Use this when a user's conversation history plus retrieved documents together risk exceeding the model's context window.
- Use this when an agent needs to reference information from previous sessions or remember user-specific facts across conversations.
- Use this when a production agent returns wrong, hallucinated, or out-of-scope outputs and you need to detect and block them automatically.
- Use this when you need to diagnose why an agent is slow and must isolate whether the bottleneck is retrieval, LLM latency, or guardrail processing.
- Use this when preparing to deploy an agent and you need to define a regression test suite that runs on every code or prompt change.
- Use this when costs are scaling unexpectedly and you need to route cheaper models for low-complexity queries.
- Use this when an agent handles sensitive user data and you must redact PII before it enters or exits the LLM.

## Concrete Examples

- Password reset query for 'Jane' (premium user): A 16,000-token budget is allocated across system prompt (200 tokens), user profile (50 tokens), retrieved docs (800 tokens), and conversation history (10 most recent messages), demonstrating context prioritization and budget arithmetic.
- ContextBuilder class with fit_docs and fit_history methods: Shows relevance-sorted doc inclusion with truncation fallback and recency-first history pruning in Python code.
- ContextCompressor with summarize_old_messages: Replaces old messages with a 3-5 bullet LLM-generated summary while keeping the N most recent messages verbatim.
- Full integrated agent run() method: Wires all 4 layers together — input guardrails, memory retrieval, context building, cost check, LLM generation, output guardrails, and memory storage — each wrapped in a named trace span.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**LLMOps Essentials**

An LLM coding agent generating agent infrastructure faces a specific failure mode: it will produce syntactically correct, plausible-looking eval suites and context builders without any grounding in what 'correct' actually means for the target domain, creating false confidence. The agent also cannot self-monitor costs or latency — without instrumented spans and budget checks baked into generated code, it will silently generate runaway-cost or slow pipelines with no observable signal. Critically, an LLM agent must treat context budget management as a first-class code constraint, not an afterthought, because it is itself subject to the same context window limits it is building around.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## LLMOps Essentials

Building an agent is the easy part. Keeping it running reliably in production — where real users depend on it, where bad outputs have consequences, and where costs compound every day — that is the hard part.

LLMOps is the discipline of operating LLM-powered systems in production. It covers four layers: context engineering, memory architecture, evaluation, and observability. Every production agent system needs all four.

---

## Why This Chapter Matters Most

Building an agent is like building a car. You can slap together an engine, wheels, and a steering wheel and drive it. But you also need:
- **A dashboard** (Layer 4: Observability) so you know if something breaks
- **Brakes** (Layer 4: Guardrails) so you don't crash
- **Maintenance schedule** (Layer 3: Evaluation) so you catch problems early
- **Fuel efficiency** (Layer 4: Cost control) so you don't bankrupt yourself
- **A memory** (Layer 2: Memory) so the car remembers where it's been
- **Good visibility out the windshield** (Layer 1: Context) so you can see the road

Skip any of these, and your car becomes a liability.

---

## The 4-Layer LLMOps Stack

```
┌─────────────────────────────────────────────────┐
│  Layer 4: OBSERVABILITY & GUARDRAILS            │  ← Can you see what's happening?
│  Traces, spans, alerts, input/output filters,   │     Can you stop it if it breaks?
│  cost tracking, drift detection                 │
├─────────────────────────────────────────────────┤
│  Layer 3: EVALUATION                            │  ← How do you know it works?
│  Unit evals, end-to-end evals,                  │     What does "good" look like?
│  LLM-as-judge, golden datasets                  │
├─────────────────────────────────────────────────┤
│  Layer 2: MEMORY ARCHITECTURE                   │  ← What does it remember?
│  In-context, episodic, semantic,                │     How long does it remember?
│  procedural memory                              │
├─────────────────────────────────────────────────┤
│  Layer 1: CONTEXT ENGINEERING                   │  ← What does it see?
│  System prompts, retrieved docs,                │     How much can it see?
│  tool results, conversation history             │
└─────────────────────────────────────────────────┘
```

---

## Layer 1: Context Engineering

**Why should I care?**

Context is literally everything the LLM can see. If your agent sees too much irrelevant information, it gets confused and gives wrong answers. If it sees too little, it can't answer the question at all. Getting this right is the difference between an agent that works and one that wastes tokens and money.

Context is everything the LLM can see at inference time. The entire context window — system prompt, retrieved docs, tool results, conversation history, structured data — is the agent's world. What is not in the context does not exist for the agent.

### The Context Budget

Every model has a context window limit. Even with 200K token models, you cannot waste tokens. More context is not always better — irrelevant context dilutes the signal and increases cost.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks "How do I reset my password?" — for the 2nd time today. The agent has a 16,000-token context budget.
>
> **INPUT:** "How do I reset my password?"
>
> **Step 1 (Gather all available context):**
>   - System prompt: "You are a support agent for Acme Corp" (200 tokens)
>   - User profile: {name: "Jane", plan: "premium", previous_tickets: 3} (50 tokens)
>   - Retrieved docs: password_reset_guide.md (800 tokens)
>   - Conversation history: 15 messages from today (2,400 tokens)
>   - Memory note: "User asked this same question 2 hours ago" (30 tokens)
>
> **Step 2 (Calculate budget):**
>   - Total available: 16,000 tokens
>   - System prompt (must include): -200 → 15,800 remaining
>   - User profile: -50 → 15,750 remaining
>   - Retrieved docs (40% budget = 6,300 max): -800 → 14,950 remaining
>   - Tool results (20% budget): 0 used → 14,950 remaining
>   - Conversation history (all remaining): keep most recent 10 messages, drop oldest 5
>
> **Step 3 (Prioritize):** Most important info goes at the beginning and end (LLMs pay more attention there).
>
> **Step 4 (Send to LLM):** Complete context package, 3,480 tokens total (well within budget).
>
> **OUTPUT to LLM:** Perfectly assembled context with system prompt first, then docs, then recent conversation.
>
> **Agent's response to user:** "Hi Jane! Since you asked about this earlier — here's the quick version: Go to Settings → Security → Reset Password. As a premium member, you can also call us at 1-800-ACME for instant help."
>
> The agent knew Jane's name, her plan, and that she asked before — all because of good context engineering.

Now let's see how this looks in code. Simple version first:

```python
def build_context_simple(system_prompt, docs, conversation):
    """Simplest possible context builder."""
    # Just put everything together
    context = system_prompt + "\n\n"
    for doc in docs:
        context += doc + "\n\n"
    for message in conversation:
        context += f"{message['role']}: {message['content']}\n"
    return context
```

**The problem:** This will exceed the token limit or include useless information.

**Better version with budgets:**

```python
class ContextBuilder:
    """
    Builds the context for each LLM call.
    
    The order matters. LLMs pay more attention to the beginning 
    and end of the context (primacy and recency effects). Put the 
    most important information first and last.
    """
    
    def __init__(self, max_tokens=16000):
        self.max_tokens = max_tokens
    
    def build(self, system_prompt, retrieved_docs, tool_results, 
              conversation_history, structured_data=None):
        
        context_parts = []
        token_budget = self.max_tokens
        
        # 1. System prompt — ALWAYS first, non-negotiable
        context_parts.append({"role": "system", "content": system_prompt})
        token_budget -= self.count_tokens(system_prompt)
        
        # 2. Structured data (if any) — user profile, settings, constraints
        if structured_data:
            data_str = self.format_structured_data(structured_data)
            context_parts.append({"role": "system", "content": data_str})
            token_budget -= self.count_tokens(data_str)
        
        # 3. Retrieved documents — most relevant context
        #    Allocate up to 40% of remaining budget
        doc_budget = int(token_budget * 0.4)
        doc_context = self.fit_docs(retrieved_docs, doc_budget)
        context_parts.append({"role": "system", "content": doc_context})
        token_budget -= self.count_tokens(doc_context)
        
        # 4. Tool results from current session
        #    Allocate up to 20% of remaining budget
        tool_budget = int(token_budget * 0.2)
        tool_context = self.fit_tool_results(tool_results, tool_budget)
        for tr in tool_context:
            context_parts.append({"role": "tool", "content": tr})
        token_budget -= sum(self.count_tokens(tr) for tr in tool_context)
        
        # 5. Conversation history — recent messages
        #    Use ALL remaining budget
        history = self.fit_history(conversation_history, token_budget)
        context_parts.extend(history)
        
        return context_parts
    
    def fit_docs(self, docs, budget):
        """
        Fit as many retrieved docs as possible within the budget.
        Strategy: Include docs in order of relevance score.
        If a doc doesn't fit, truncate it or skip it.
        """
        fitted = []
        used = 0
        
        for doc in sorted(docs, key=lambda d: d.score, reverse=True):
            doc_tokens = self.count_tokens(doc.text)
            
            if used + doc_tokens <= budget:
                fitted.append(doc.text)
                used += doc_tokens
            elif budget - used > 200:
                # Truncate this doc to fill remaining space
                truncated = self.truncate_to_tokens(doc.text, budget - used)
                fitted.append(truncated + "\n[truncated]")
                break
            else:
                break
        
        return "\n\n---\n\n".join(fitted)
    
    def fit_history(self, history, budget):
        """
        Fit conversation history within budget.
        Strategy: Keep the MOST RECENT messages. Drop old ones.
        
        Why recent? Because the user's most recent messages are 
        most relevant to what they want NOW. Old messages are 
        context, but recent messages are the actual task.
        """
        fitted = []
        used = 0
        
        # Walk backwards from most recent
        for msg in reversed(history):
            msg_tokens = self.count_tokens(msg["content"])
            if used + msg_tokens <= budget:
                fitted.insert(0, msg)
                used += msg_tokens
            else:
                break
        
        return fitted
```

**Line-by-line explanation (key parts):**

1. `def __init__(self, max_tokens=16000):` → Store the max token limit
2. `token_budget = self.max_tokens` → Start with the full budget
3. `context_parts.append({"role": "system", "content": system_prompt})` → Add the system prompt (never skip this)
4. `token_budget -= self.count_tokens(system_prompt)` → Subtract what we used from the budget
5. `doc_budget = int(token_budget * 0.4)` → Allocate 40% of remaining budget to docs
6. `self.fit_docs(retrieved_docs, doc_budget)` → Fit as many docs as possible within that budget
7. `for doc in sorted(docs, key=lambda d: d.score, reverse=True):` → Sort docs by relevance (highest first)
8. `if used + doc_tokens <= budget:` → Check if this doc fits
9. `elif budget - used > 200:` → If we have room for a partial doc, truncate and include it
10. `for msg in reversed(history):` → Walk backwards through conversation (most recent first)
11. `fitted.insert(0, msg)` → Insert at the beginning (so we end up in correct order)

---

### Context Compression Strategies

When the context window fills up, you need compression:

```python
class ContextCompressor:
    
    def summarize_old_messages(self, messages, keep_recent=5):
        """
        Replace old messages with a summary.
        Keep the N most recent messages verbatim.
        """
        old_messages = messages[:-keep_recent]
        recent_messages = messages[-keep_recent:]
        
        summary = self.llm.generate(
            prompt=f"""Summarize this conversation history in 3-5 bullet points.
            Focus on: key decisions made, important facts mentioned, 
            and the user's current goal.
            
            Messages:
            {self.format_messages(old_messages)}"""
        )
        
        return [
            {"role": "system", "content": f"Conversation summary:\n{summary}"}
        ] + recent_messages
    
    def selective_retrieval(self, query, all_docs, max_docs=5):
        """
        Instead of stuffing all docs into context, retrieve only 
        the most relevant ones for the current query.
        
        This is what makes agentic RAG different from naive RAG.
        """
        relevant = self.retriever.retrieve(query, top_k=max_docs)
        return relevant
```

---

## Layer 2: Memory Architecture

**Why should I care?**

Without memory, your agent has amnesia. Every conversation starts from zero. The user says "Remember what I told you yesterday?" and your agent has no idea what they're talking about. Memory lets agents learn about users and improve over time.

Memory is how the agent retains information beyond a single request. There are four types, and most production systems use at least two.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** It's conversation turn 5. The user says "Use the same format as last time."
>
> **INPUT:** "Use the same format as last time"
>
> **Step 1 (In-context memory — check current conversation):**
>   - Turn 1: User asked for a sales report
>   - Turn 2: Agent delivered as bullet points
>   - Turn 3: User said "Perfect, I love bullet points!"
>   - Turn 4: User asked about a different topic
>   → Found: "last time" = bullet point format ✓
>
> **Step 2 (Episodic memory — check past sessions):**
>   - Search vector DB for this user's preferences
>   - Found: "This user prefers concise answers" (from 15 past sessions)
>   - Found: "User works in marketing" (from profile)
>   → Lessons: Keep it concise, use business language ✓
>
> **Step 3 (Semantic memory — check knowledge base):**
>   - Not needed for this request (no factual lookup required)
>   → Skipped ✓
>
> **Step 4 (Procedural memory — check for specific processes):**
>   - No matching procedure for "formatting preferences"
>   → Skipped ✓
>
> **Step 5 (Combine memories into context):**
>   - Format: bullet points (from in-context memory)
>   - Style: concise (from episodic memory)
>   - Domain: marketing language (from episodic memory)
>
> **OUTPUT:** Agent responds with concise bullet points in business language — exactly what the user wanted.
>
> Without memory, the agent would have asked "What format would you like?" — frustrating for the user who already told it.

Now let's look at how memory is structured in code:

### The 4 Memory Types

```python
class MemorySystem:
    """
    Four types of memory, each serving a different purpose.
    """
    
    def __init__(self):
        # TYPE 1: In-context memory
        # Lives inside the LLM's context window. Dies when the session ends.
        # The current conversation.
        self.in_context = []
        
        # TYPE 2: Episodic memory (external)
        # Past interactions stored in a vector DB. Survives across sessions.
        # "The user prefers concise answers" / "Last time they asked about X"
        self.episodic = VectorStore(collection="episodic_memory")
        
        # TYPE 3: Semantic memory
        # Facts, documents, knowledge. The agent's reference library.
        # Product catalog, company policies, technical documentation.
        self.semantic = VectorStore(collection="knowledge_base")
        
        # TYPE 4: Procedural memory
        # How to do things. Stored as prompts, tool schemas, or code.
        # "When the user asks about refunds, follow this 5-step process"
        self.procedural = {
            "refund_process": "Step 1: Verify order. Step 2: Check eligibility...",
            "escalation_rules": "Escalate if: customer mentions lawyer, ...",
        }
    
    def get_relevant_memories(self, query, user_id=None):
        """
        Pull relevant memories from all stores for the current query.
        """
        memories = {}
        
        # Episodic: What do we know about this user?
        if user_id:
            memories["episodic"] = self.episodic.search(
                query=query,
                filter={"user_id": user_id},
                top_k=3
            )
        
        # Semantic: What facts are relevant?
        memories["semantic"] = self.semantic.search(
            query=query,
            top_k=5
        )
        
        # Procedural: Is there a specific process for this type of request?
        memories["procedural"] = self.match_procedure(query)
        
        return memories
    
    def store_interaction(self, user_id, interaction):
        """
        After each interaction, store what we learned.
        
        Be selective — not every message is worth storing.
        Store: preferences, corrections, important facts.
        Don't store: greetings, acknowledgments, noise.
        """
        should_store = self.llm.generate(
            prompt=f"""Should this interaction be stored in long-term memory?
            
            Interaction: {interaction}
            
            Store if it contains: user preferences, corrections to our behavior,
            important facts about the user, or decisions made.
            
            Don't store if it's: a greeting, acknowledgment, or routine exchange.
            
            Return: STORE or SKIP, plus a one-sentence summary if STORE."""
        )
        
        if "STORE" in should_store:
            self.episodic.upsert({
                "user_id": user_id,
                "summary": should_store.split("STORE")[1].strip(),
                "timestamp": datetime.now(),
                "raw": interaction
            })
```

**Line-by-line explanation:**

1. `self.in_context = []` → Start with empty conversation (cleared each session)
2. `self.episodic = VectorStore(collection="episodic_memory")` → Create a vector store for user-specific memories
3. `self.semantic = VectorStore(collection="knowledge_base")` → Create a vector store for general knowledge
4. `self.procedural = {...}` → Create a dictionary for step-by-step processes
5. `if user_id: memories["episodic"] = self.episodic.search(...)` → Search episodic memory for this specific user
6. `memories["semantic"] = self.semantic.search(...)` → Search semantic memory (not user-specific)
7. `memories["procedural"] = self.match_procedure(query)` → Find relevant procedures

---

## Layer 3: Evaluation (Evals)

**Why should I care?**

If you don't evaluate your agent, you're guessing whether it works. You're flying blind. Most AI projects fail because they ship without evals and then discover in production that the agent gives wrong answers. Evals are your insurance policy.

If you do not evaluate your agent, you are guessing whether it works. Evals are the tests of the LLM world.

### Stop and Think

Before we code, think: "What would it look like if my agent gave the wrong answer?" Write down 5 specific examples. Those examples are the start of your test cases.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** You've built a customer support agent. Before deploying, you run it against 3 test cases from your golden dataset.
>
> **INPUT:** Run evaluation on 3 test cases.
>
> **Test Case 1: "What's our return policy?"**
>   - Expected answer: "30-day return policy for unused items"
>   - Agent's answer: "You can return items within 30 days if unused"
>   - Exact match: No (different words)
>   - Semantic match: Yes (same meaning) ✓
>   - LLM-as-Judge score: 4.8/5.0 — PASS ✓
>
> **Test Case 2: "Who is the CEO?"**
>   - Expected answer: "Jane Smith"
>   - Agent's answer: "The CEO is John Smith"
>   - Exact match: No
>   - Semantic match: No (WRONG NAME!) ✗
>   - LLM-as-Judge score: 1.0/5.0 — FAIL ✗ 🚨
>   - Investigation: Knowledge base has outdated CEO name
>
> **Test Case 3: "What are your hours?"**
>   - Expected answer: "9 AM to 5 PM EST"
>   - Agent's answer: "We're open 9-5 Eastern time"
>   - Semantic match: Yes ✓
>   - LLM-as-Judge score: 4.5/5.0 — PASS ✓
>
> **EVALUATION SUMMARY:**
> ```
> Results: 2/3 passed (66.7%)
> 
> ✓ return_policy: PASS (4.8/5.0)
> ✗ ceo_name:      FAIL (1.0/5.0) — CRITICAL: wrong factual answer
> ✓ business_hours: PASS (4.5/5.0)
> 
> Action needed: Update CEO entry in knowledge base
> ```
>
> Without evals, you would have deployed and a real customer would have gotten the wrong CEO name. Evals caught it first.

Now let's see how to build these evaluations in code:

### Pattern: Unit Eval vs End-to-End Eval

```python
# --- SIMPLE VERSION FIRST: A single test case ---

def test_single_case():
    """Test one thing: does the retriever find the right doc?"""
    query = "What is our refund policy?"
    retrieved = retriever.retrieve(query, top_k=5)
    retrieved_ids = [r.id for r in retrieved]
    
    # We know the answer should be in doc 42
    assert "doc_42" in retrieved_ids, "Failed to retrieve correct doc"
    print("✓ Retrieval test passed")

# --- CLASS VERSION: Reusable test framework ---
```

### Types of Evals

```python
# --- TYPE 1: UNIT EVALS ---
# Test a single step in isolation. Does the retriever find the right docs?
# Does the classifier pick the right category?

class UnitEval:
    """Test one component in isolation."""
    
    def eval_retriever(self, retriever, test_cases):
        """
        Does the retriever find the right documents?
        
        Test case format:
        {"query": "What is our refund policy?", 
         "expected_doc_ids": ["doc_42", "doc_78"]}
        """
        results = []
        for case in test_cases:
            retrieved = retriever.retrieve(case["query"], top_k=5)
            retrieved_ids = [r.id for r in retrieved]
            
            recall = len(
                set(case["expected_doc_ids"]) & set(retrieved_ids)
            ) / len(case["expected_doc_ids"])
            
            results.append({
                "query": case["query"],
                "recall": recall,
                "pass": recall >= 0.8  # At least 80% of expected docs found
            })
        
        return results
    
    def eval_classifier(self, classifier, test_cases):
        """
        Does the classifier pick the right category?
        """
        correct = 0
        for case in test_cases:
            predicted = classifier.classify(case["input"])
            if predicted == case["expected_category"]:
                correct += 1
        
        accuracy = correct / len(test_cases)
        return {"accuracy": accuracy, "pass": accuracy >= 0.9}


# --- TYPE 2: END-TO-END EVALS ---
# Test the full pipeline. Does the agent answer the user's question correctly?

class EndToEndEval:
    """Test the entire agent pipeline from input to output."""
    
    def eval_agent(self, agent, test_cases):
        """
        Run the full agent and check if the output is acceptable.
        
        Test case format:
        {"input": "What is our refund policy for digital products?",
         "expected_answer_contains": ["14 days", "no questions asked"],
         "must_cite": True,
         "max_latency_ms": 5000}
        """
        results = []
        for case in test_cases:
            start = time.time()
            output = agent.run(case["input"])
            latency = (time.time() - start) * 1000
            
            # Check answer quality
            contains_expected = all(
                phrase in output["answer"] 
                for phrase in case.get("expected_answer_contains", [])
            )
            
            # Check citations
            has_citations = bool(output.get("sources")) if case.get("must_cite") else True
            
            # Check latency
            within_latency = latency <= case.get("max_latency_ms", 10000)
            
            results.append({
                "input": case["input"],
                "pass": contains_expected and has_citations and within_latency,
                "details": {
                    "answer_correct": contains_expected,
                    "has_citations": has_citations,
                    "latency_ms": latency,
                    "within_latency": within_latency
                }
            })
        
        return results


# --- TYPE 3: LLM-AS-JUDGE ---
# Use an LLM to evaluate another LLM's output. Faster than human labels,
# cheaper than hiring annotators, and surprisingly reliable when calibrated.

class LLMJudge:
    """Use a strong LLM to evaluate agent outputs."""
    
    def __init__(self, judge_llm):
        self.judge = judge_llm
    
    def evaluate(self, question, agent_answer, reference_docs=None):
        """
        Score the agent's answer on multiple dimensions.
        """
        judge_prompt = f"""You are an expert evaluator. Score this AI agent's 
        answer on a scale of 1-5 for each dimension.
        
        Question: {question}
        Agent's Answer: {agent_answer}
        {"Reference Documents: " + str(reference_docs) if reference_docs else ""}
        
        Score each dimension:
        
        1. CORRECTNESS (1-5): Is the answer factually correct?
           1 = Completely wrong
           3 = Partially correct with some errors  
           5 = Fully correct
        
        2. COMPLETENESS (1-5): Does the answer fully address the question?
           1 = Misses the main point entirely
           3 = Addresses the question but misses important details
           5 = Comprehensive answer
        
        3. GROUNDEDNESS (1-5): Is the answer supported by the provided documents?
           1 = Makes claims with no support
           3 = Some claims supported, some not
           5 = Every claim is supported by evidence
        
        4. HELPFULNESS (1-5): Would a user find this answer useful?
           1 = Not helpful at all
           3 = Somewhat helpful
           5 = Exactly what the user needed
        
        Return JSON:
        {{
            "correctness": X,
            "completeness": X,
            "groundedness": X,
            "helpfulness": X,
            "overall": X,
            "reasoning": "one sentence explaining the overall score"
        }}"""
        
        scores = json.loads(self.judge.generate(prompt=judge_prompt))
        return scores
```

**Line-by-line explanation (EndToEndEval):**

1. `def eval_agent(self, agent, test_cases):` → Method to test the full agent
2. `for case in test_cases:` → Loop through each test case
3. `start = time.time()` → Record the start time
4. `output = agent.run(case["input"])` → Run the agent with this input
5. `latency = (time.time() - start) * 1000` → Calculate how long it took (in milliseconds)
6. `contains_expected = all(phrase in output["answer"] for phrase in case.get(...))` → Check if the answer contains all expected phrases
7. `has_citations = bool(output.get("sources"))` → Check if the output has sources (citations)
8. `within_latency = latency <= case.get("max_latency_ms", 10000)` → Check if it was fast enough
9. `results.append({...})` → Store the result (pass or fail)

---

### Building a Golden Dataset

A golden dataset is your ground truth — human-verified question-answer pairs that define what "correct" looks like.

```python
class GoldenDataset:
    """
    A curated set of test cases with human-verified correct answers.
    
    Building a golden dataset:
    1. Collect real user questions from production logs
    2. Have domain experts write the correct answers
    3. Include edge cases: ambiguous questions, questions with no answer,
       questions that span multiple documents
    4. Update regularly as the knowledge base changes
    5. Aim for 100-500 test cases covering all important scenarios
    """
    
    def __init__(self):
        self.test_cases = []
    
    def add_case(self, question, correct_answer, category, difficulty, 
                 source_docs=None, notes=None):
        self.test_cases.append({
            "question": question,
            "correct_answer": correct_answer,
            "category": category,       # e.g., "refund_policy", "product_specs"
            "difficulty": difficulty,    # "easy", "medium", "hard", "adversarial"
            "source_docs": source_docs,  # Which docs contain the answer
            "notes": notes,             # Special considerations
            "added_date": datetime.now(),
            "last_verified": datetime.now()
        })
    
    def run_eval(self, agent, judge=None):
        """Run the full golden dataset evaluation."""
        results = {"pass": 0, "fail": 0, "by_category": {}, "by_difficulty": {}}
        
        for case in self.test_cases:
            agent_answer = agent.run(case["question"])
            
            if judge:
                scores = judge.evaluate(
                    case["question"], agent_answer, case.get("source_docs")
                )
                passed = scores["overall"] >= 4
            else:
                passed = self.string_match(agent_answer, case["correct_answer"])
            
            results["pass" if passed else "fail"] += 1
            
            # Track by category
            cat = case["category"]
            if cat not in results["by_category"]:
                results["by_category"][cat] = {"pass": 0, "fail": 0}
            results["by_category"][cat]["pass" if passed else "fail"] += 1
        
        results["pass_rate"] = results["pass"] / len(self.test_cases)
        return results
```

---

### Walkthrough: One Complete Test Case End-to-End

Let's build ONE specific test case from scratch and run it:

```python
# Step 1: Define the test case
test_case = {
    "input": "What is your refund policy for digital products?",
    "expected_answer_contains": ["14 days", "no questions asked", "full refund"],
    "must_cite": True,
    "max_latency_ms": 3000
}

# Step 2: Run the agent
import time
start = time.time()
output = agent.run(test_case["input"])
latency_ms = (time.time() - start) * 1000

# Example output:
# {
#     "answer": "We offer a 14-day refund window for digital products with no questions asked. You get a full refund if you request it within 14 days of purchase.",
#     "sources": ["docs/refund-policy.md"]
# }

# Step 3: Check each criterion
print("=== TEST CASE RESULTS ===\n")

# Check 1: Does the answer contain all required phrases?
contains_all = all(
    phrase in output["answer"] 
    for phrase in test_case["expected_answer_contains"]
)
print(f"✓ Contains all required phrases: {contains_all}")
if not contains_all:
    missing = [
        phrase for phrase in test_case["expected_answer_contains"]
        if phrase not in output["answer"]
    ]
    print(f"  Missing: {missing}")

# Check 2: Does it have citations?
has_sources = bool(output.get("sources"))
print(f"✓ Has citations: {has_sources}")
if not has_sources and test_case["must_cite"]:
    print("  FAIL: Citations required but missing")

# Check 3: Is it fast enough?
within_budget = latency_ms <= test_case["max_latency_ms"]
print(f"✓ Within latency budget: {within_budget}")
print(f"  Latency: {latency_ms:.1f}ms (budget: {test_case['max_latency_ms']}ms)")

# Overall result
all_pass = contains_all and has_sources and within_budget
print(f"\nOVERALL: {'PASS ✓' if all_pass else 'FAIL ✗'}")
```

**Output:**
```
=== TEST CASE RESULTS ===

✓ Contains all required phrases: True
✓ Has citations: True
✓ Within latency budget: True
  Latency: 487.3ms (budget: 3000ms)

OVERALL: PASS ✓
```

---

## Layer 4: Observability & Guardrails

**Why should I care?**

When your agent breaks at 2am and customers are calling, how do you figure out what went wrong? You don't have a "replay" button. You can't step through code like a human programmer. All you have are logs and traces. Without observability, you're debugging blind.

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user sends a request: "Summarize this document." Your production agent processes it while the tracer records every step.
>
> **INPUT:** "Summarize this document" + attached 5-page PDF
>
> **The request flows through the system. Here's what the tracer records:**
>
> ```
> TRACE ID: trace_abc123 (total: 1,890ms, cost: $0.0234)
>   ├─ Span 1: receive_request (2ms)
>   │   → Logged: user_id=jane_42, request_text, timestamp
>   │
>   ├─ Span 2: input_guardrails (18ms)
>   │   → PII check: passed ✓
>   │   → Topic check: passed ✓
>   │
>   ├─ Span 3: retrieve_docs (145ms)
>   │   → Searched vector DB, found 3 relevant chunks
>   │   → Logged: query, num_results=3, relevance_scores
>   │
>   ├─ Span 4: build_context (12ms)
>   │   → Context size: 2,400 tokens (within 16K budget)
>   │
>   ├─ Span 5: call_llm (1,647ms) ← SLOWEST STEP
>   │   → Model: claude-sonnet, input: 2,400 tokens, output: 350 tokens
>   │   → Cost: $0.0198
>   │
>   ├─ Span 6: output_guardrails (23ms)
>   │   → Hallucination check: passed ✓
>   │   → PII in output check: passed ✓
>   │
>   └─ Span 7: return_response (3ms)
>       → Total time: 1,890ms, status: success
> ```
>
> **OUTPUT:** The user gets their summary. You get a complete trace showing every step, its duration, and its cost.
>
> **Why this matters:** Next day, a request takes 15 seconds instead of 2. You pull up the trace and see: Span 3 (retrieve_docs) took 12,000ms. The vector database is overloaded. Without the trace, you'd be guessing.

Now let's see how to build this tracing system:

### Traces and Spans

A **trace** is the full log of one agent run from start to finish. A **span** is one step within that trace.

```python
class Tracer:
    """
    Records every step of an agent's execution.
    
    This is how you debug a multi-agent system in production.
    Without traces, you are debugging blind.
    """
    
    def __init__(self):
        self.traces = {}
    
    def start_trace(self, request_id, user_input):
        self.traces[request_id] = {
            "id": request_id,
            "start_time": datetime.now(),
            "input": user_input,
            "spans": [],
            "total_tokens": 0,
            "total_cost": 0.0
        }
    
    def start_span(self, request_id, span_name, span_type):
        """
        Start tracking one step within the trace.
        
        span_type: "llm_call", "tool_call", "retrieval", "routing"
        """
        span = {
            "name": span_name,
            "type": span_type,
            "start_time": datetime.now(),
            "end_time": None,
            "input": None,
            "output": None,
            "tokens": 0,
            "cost": 0.0,
            "status": "running"
        }
        self.traces[request_id]["spans"].append(span)
        return len(self.traces[request_id]["spans"]) - 1  # span index
    
    def end_span(self, request_id, span_index, output, tokens=0, cost=0.0):
        span = self.traces[request_id]["spans"][span_index]
        span["end_time"] = datetime.now()
        span["output"] = output
        span["tokens"] = tokens
        span["cost"] = cost
        span["status"] = "completed"
        span["duration_ms"] = (span["end_time"] - span["start_time"]).total_seconds() * 1000
        
        # Update trace totals
        self.traces[request_id]["total_tokens"] += tokens
        self.traces[request_id]["total_cost"] += cost
    
    def get_trace_summary(self, request_id):
        """
        Human-readable summary of what happened during this request.
        
        Example output:
        Trace abc-123 (1,234ms total, $0.0082)
          ├─ [retrieval] search_docs (145ms, 0 tokens)
          ├─ [llm_call] generate_answer (876ms, 1,542 tokens, $0.0046)
          ├─ [llm_call] critique_answer (198ms, 423 tokens, $0.0013)
          └─ [llm_call] final_revision (15ms, 256 tokens, $0.0008)
        """
        trace = self.traces[request_id]
        lines = [f"Trace {request_id} ({self.total_duration(trace)}ms total, ${trace['total_cost']:.4f})"]
        
        for i, span in enumerate(trace["spans"]):
            prefix = "└─" if i == len(trace["spans"]) - 1 else "├─"
            lines.append(
                f"  {prefix} [{span['type']}] {span['name']} "
                f"({span.get('duration_ms', 0):.0f}ms, "
                f"{span['tokens']} tokens, ${span['cost']:.4f})"
            )
        
        return "\n".join(lines)
```

**Line-by-line explanation:**

1. `def start_trace(self, request_id, user_input):` → Start recording a new trace for this request
2. `self.traces[request_id] = {...}` → Create a trace object with metadata
3. `def start_span(self, request_id, span_name, span_type):` → Mark the start of a step
4. `span = {"name": span_name, ...}` → Create a span object
5. `self.traces[request_id]["spans"].append(span)` → Add this span to the trace
6. `return len(self.traces[request_id]["spans"]) - 1` → Return the index (we'll need it later to end_span)
7. `def end_span(self, request_id, span_index, output, tokens=0, cost=0.0):` → Mark the end of a step
8. `span = self.traces[request_id]["spans"][span_index]` → Get the span we created earlier
9. `span["duration_ms"] = (span["end_time"] - span["start_time"]).total_seconds() * 1000` → Calculate how long it took
10. `self.traces[request_id]["total_tokens"] += tokens` → Update the total token count

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user sends a message to your customer support agent that contains sensitive information AND an out-of-scope request.
>
> **INPUT:** "My SSN is 123-45-6789 and my email is jane@example.com. Can you help me file my taxes?"
>
> **Step 1 (Input Guardrail #1 — PII Detection):**
>   - Scans the message for personal information
>   - FOUND: SSN pattern (XXX-XX-XXXX) at position 10 → `123-45-6789`
>   - FOUND: Email pattern at position 40 → `jane@example.com`
>   - ACTION: Redact both → "My SSN is [REDACTED_SSN] and my email is [REDACTED_EMAIL]. Can you help me file my taxes?"
>   - Message is modified, not blocked. Continues to next guardrail. ➡️
>
> **Step 2 (Input Guardrail #2 — Topic Check):**
>   - Analyzes: "Can you help me file my taxes?"
>   - Detects topic: `tax_advice`
>   - Allowed topics: `[product_support, billing, account_management]`
>   - `tax_advice` is NOT in the allowed list
>   - ACTION: **BLOCKED** 🚫
>   - The request NEVER reaches the LLM. It stops here.
>
> **Step 3 (No agent execution — request was blocked)**
>
> **OUTPUT to user:**
> ```
> "I'm not able to help with tax filing — that's outside what I'm designed to do. 
> For tax advice, please consult a qualified tax professional.
> 
> I can help with your account, billing, or product questions!
> 
> Also, I noticed you shared sensitive information (SSN and email). 
> I've removed it from this conversation for your safety."
> ```
>
> Two guardrails worked together: PII Guard cleaned the data, Topic Guard blocked the request. The LLM never saw the user's SSN.

Now let's see how to build guardrails, starting with the simplest version:

### Guardrails: Simple Version First

Before we build a complex guardrail system, let's start with the simplest possible PII check:

```python
# --- SIMPLEST VERSION: Just regex ---

import re

def detect_pii_simple(text):
    """Check if text contains PII (personal info) using simple regex."""
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    }
    
    found = {}
    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            found[pii_type] = matches
    
    return found

# --- USE IT ---
text = "Call me at 555-123-4567 or email john@example.com"
pii = detect_pii_simple(text)
print(f"Found PII: {pii}")
# Output: Found PII: {'phone': ['555-123-4567'], 'email': ['john@example.com']}
```

---

### Guardrails: Class Version

```python
class GuardrailPipeline:
    """
    Input guardrails → Agent → Output guardrails
    
    Guardrails run BEFORE and AFTER the agent.
    They can block, modify, or flag content.
    """
    
    def __init__(self, input_guards, output_guards, agent):
        self.input_guards = input_guards
        self.output_guards = output_guards
        self.agent = agent
    
    def run(self, user_input):
        # --- INPUT GUARDRAILS ---
        for guard in self.input_guards:
            result = guard.check(user_input)
            if result.blocked:
                return {
                    "status": "blocked",
                    "reason": result.reason,
                    "guardrail": guard.name
                }
            if result.modified:
                user_input = result.modified_input  # e.g., PII redacted
        
        # --- AGENT EXECUTION ---
        agent_output = self.agent.run(user_input)
        
        # --- OUTPUT GUARDRAILS ---
        for guard in self.output_guards:
            result = guard.check(agent_output)
            if result.blocked:
                return {
                    "status": "blocked",
                    "reason": "Output failed safety check",
                    "guardrail": guard.name,
                    "fallback": guard.get_fallback_response()
                }
            if result.modified:
                agent_output = result.modified_output
        
        return {"status": "success", "output": agent_output}


# --- EXAMPLE GUARDRAILS ---

class PIIGuard:
    """Detects and redacts personally identifiable information."""
    name = "pii_guard"
    
    def check(self, text):
        pii_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        }
        
        found_pii = []
        redacted = text
        for pii_type, pattern in pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                found_pii.append(pii_type)
                redacted = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", redacted)
        
        if found_pii:
            return GuardResult(modified=True, modified_input=redacted)
        return GuardResult(passed=True)


class TopicGuard:
    """Blocks requests that are outside the agent's scope."""
    name = "topic_guard"
    
    def __init__(self, llm, allowed_topics):
        self.llm = llm
        self.allowed_topics = allowed_topics
    
    def check(self, text):
        is_on_topic = self.llm.generate(
            prompt=f"""Is this request about one of these topics: {self.allowed_topics}?
            
            Request: {text}
            
            Return YES or NO."""
        )
        
        if "NO" in is_on_topic:
            return GuardResult(
                blocked=True,
                reason=f"Request is outside allowed topics: {self.allowed_topics}"
            )
        return GuardResult(passed=True)


class HallucinationGuard:
    """Checks if the agent's response is grounded in provided evidence."""
    name = "hallucination_guard"
    
    def __init__(self, llm):
        self.llm = llm
    
    def check(self, response):
        if not response.get("sources"):
            return GuardResult(passed=True)  # No sources to check against
        
        grounded = self.llm.generate(
            prompt=f"""Check if every claim in this response is supported 
            by the provided sources.
            
            Response: {response['answer']}
            Sources: {response['sources']}
            
            For each claim, mark it as SUPPORTED or UNSUPPORTED.
            If any claim is UNSUPPORTED, return FAIL.
            Otherwise return PASS."""
        )
        
        if "FAIL" in grounded:
            return GuardResult(
                blocked=True,
                reason="Response contains claims not supported by sources"
            )
        return GuardResult(passed=True)
```

---

### Cost Control

```python
class CostTracker:
    """
    Track and control LLM API costs.
    
    Without cost tracking, a busy agent can run up a $10,000 bill 
    in a day. This happens. Budget limits are not optional.
    """
    
    def __init__(self, daily_budget, per_request_budget):
        self.daily_budget = daily_budget          # e.g., $100/day
        self.per_request_budget = per_request_budget  # e.g., $0.50/request
        self.daily_spend = 0.0
        self.last_reset = datetime.now().date()
    
    # Model pricing (per 1K tokens, approximate)
    PRICING = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "claude-sonnet": {"input": 0.003, "output": 0.015},
        "claude-haiku": {"input": 0.00025, "output": 0.00125},
    }
    
    def check_budget(self, estimated_tokens, model):
        """Call this BEFORE making an LLM call."""
        self.maybe_reset_daily()
        
        estimated_cost = self.estimate_cost(estimated_tokens, model)
        
        if self.daily_spend + estimated_cost > self.daily_budget:
            raise BudgetExceededError(
                f"Daily budget ${self.daily_budget} would be exceeded. "
                f"Spent: ${self.daily_spend:.2f}, Estimated: ${estimated_cost:.4f}"
            )
        
        return True
    
    def route_to_cheapest_model(self, task_complexity):
        """
        Model routing: Use cheap models for simple tasks, 
        expensive models only when needed.
        
        This alone can cut costs by 50-70%.
        """
        if task_complexity == "simple":
            return "gpt-4o-mini"     # Classification, routing, simple extraction
        elif task_complexity == "medium":
            return "claude-haiku"     # Summarization, Q&A with context
        else:
            return "claude-sonnet"    # Complex reasoning, planning, reflection
```

---

## Putting It All Together

Here is what a production-ready agent looks like when you combine all four layers:

```python
class ProductionAgent:
    """
    A production-ready agent with all 4 LLMOps layers.
    This is what real systems look like (simplified).
    """
    
    def __init__(self, llm, retriever, memory, tracer, guardrails, cost_tracker):
        self.llm = llm
        self.retriever = retriever
        self.memory = memory
        self.tracer = tracer
        self.guardrails = guardrails
        self.cost_tracker = cost_tracker
    
    def run(self, user_input, user_id, request_id):
        # START TRACE
        self.tracer.start_trace(request_id, user_input)
        
        # LAYER 4: INPUT GUARDRAILS
        guard_span = self.tracer.start_span(request_id, "input_guardrails", "guardrail")
        guard_result = self.guardrails.check_input(user_input)
        self.tracer.end_span(request_id, guard_span, guard_result)
        
        if guard_result.blocked:
            return guard_result.fallback_response
        
        # LAYER 2: RETRIEVE MEMORIES
        mem_span = self.tracer.start_span(request_id, "memory_retrieval", "retrieval")
        memories = self.memory.get_relevant_memories(user_input, user_id)
        self.tracer.end_span(request_id, mem_span, f"{len(memories)} memories retrieved")
        
        # LAYER 1: BUILD CONTEXT
        ctx_span = self.tracer.start_span(request_id, "context_build", "processing")
        retrieved_docs = self.retriever.retrieve(user_input)
        context = self.context_builder.build(
            system_prompt=self.system_prompt,
            retrieved_docs=retrieved_docs,
            tool_results=[],
            conversation_history=memories.get("episodic", []),
        )
        self.tracer.end_span(request_id, ctx_span, f"{len(context)} context parts")
        
        # COST CHECK
        self.cost_tracker.check_budget(estimated_tokens=4000, model=self.model_name)
        
        # AGENT EXECUTION (the actual LLM call)
        llm_span = self.tracer.start_span(request_id, "llm_generate", "llm_call")
        response = self.llm.generate(messages=context)
        self.tracer.end_span(request_id, llm_span, response, 
                            tokens=response.usage.total, 
                            cost=self.cost_tracker.compute_cost(response.usage))
        
        # LAYER 4: OUTPUT GUARDRAILS
        out_span = self.tracer.start_span(request_id, "output_guardrails", "guardrail")
        output_check = self.guardrails.check_output(response.content)
        self.tracer.end_span(request_id, out_span, output_check)
        
        if output_check.blocked:
            return output_check.fallback_response
        
        # LAYER 2: STORE INTERACTION
        self.memory.store_interaction(user_id, {
            "question": user_input,
            "answer": response.content,
            "request_id": request_id
        })
        
        # LOG TRACE
        print(self.tracer.get_trace_summary(request_id))
        
        return response.content
```

---

## In Production, This Looks Like...

A real LLMOps project structure:

```
my_ai_project/
├── evals/
│   ├── golden_dataset.json      # 200 verified test cases
│   ├── unit_eval_retriever.py   # Test retriever accuracy
│   ├── e2e_eval_agent.py        # Test full agent
│   └── judge.py                 # LLM-as-judge implementation
├── guardrails/
│   ├── pii_guard.py             # Detect and redact PII
│   ├── topic_guard.py           # Enforce scope
│   ├── hallucination_guard.py   # Check groundedness
│   └── pipeline.py              # Combine all guards
├── monitoring/
│   ├── tracer.py                # Record traces and spans
│   ├── cost_tracker.py          # Track spending
│   └── dashboards.py            # Visualize health
├── agent.py                     # The main agent
└── run_evals.py                 # Script: python run_evals.py
```

**Run evals every time you change the system:**
```bash
python run_evals.py
# Output:
# ✓ Retriever: 92% accuracy
# ✓ Agent: 87% pass rate on golden dataset
# ✓ Guardrails: 0 hallucinations detected
# Cost estimate: $0.043 per request
```

---

## Developing Your AI Capability

At this stage, AI can help you:
- **Write eval test cases** (give AI 10 examples of good answers, ask it to generate 20 more test cases)
- **Draft guardrail rules** (AI can generate regex patterns or LLM prompts for guardrails)
- **Generate monitoring dashboards** (AI can write the code to visualize traces and costs)
- **Calculate token budgets** (AI can estimate tokens for your context components)

But **YOU must understand:**
- **Why you need evals** (this is the #1 thing people skip and regret). You MUST know what "correct" looks like BEFORE you go to production
- **What a trace tells you** (when your agent breaks, you read the trace. You need to know how to interpret it)
- **How costs add up** (10 requests/second × $0.01/request × 24 hours = $8,640/day. This happens to real companies)
- **The failure modes** (what happens if the retriever fails? If guardrails fail? If the LLM is slow? You need to handle each)

### The LLM Fallacy

Here's the trap: You ask AI to generate your evals. It writes 50 test cases. They look reasonable. You don't really understand what they're testing. You run them against your agent. 90% pass.

Then you deploy. A user finds a case that breaks the agent. It's not in your evals because you didn't actually think through what matters.

**The check:** Can you write down on paper what "correct" means for your system WITHOUT AI help? If not, you don't understand the problem yet. AI can help you implement evals, but YOU have to define what good looks like.

---

## Exercises

### Exercise 1: Build One Golden Test Case

Pick ONE important question your agent should answer. Write:
1. The exact question
2. What the correct answer should contain
3. What would count as wrong
4. How fast should it respond
5. Should it have citations?

Don't use AI. You're defining what "correct" means for your domain.

### Exercise 2: Design an Evaluation

For the test case you just wrote, design:
1. What would you check automatically (latency, citations)?
2. What would you need a human to judge?
3. How would you test edge cases (typos, ambiguous wording)?
4. How often would you run this test?

### Exercise 3: Trace a Failure

Imagine your agent is slow (taking 30 seconds instead of 2 seconds). Write down:
1. Where in the pipeline might it be slow? (retrieval? LLM? guardrails?)
2. How would you use traces to find out?
3. What would each span's duration tell you?
4. What would you do to fix it?

---

## What You Should Be Able to Do Now

After reading this chapter, you should be able to:

1. Build a context window with proper priority ordering and budget management
2. Design a memory system with all 4 memory types
3. Write unit evals, end-to-end evals, and LLM-as-judge evaluations
4. Build a golden dataset and run regression tests
5. Implement tracing with spans for debugging multi-agent systems
6. Set up input and output guardrails (PII, topic, hallucination)
7. Track costs and implement model routing to control spending
8. Put all 4 layers together into a production-ready agent
9. Explain why evals are non-negotiable (not optional)

Next: [Design Your First Agent →](../first-agent/01-design-walkthrough.md)

---

## TraceSpan Observability Instrumenting each pipeline stage as named spans within

## Core Principle

LLMOps is the discipline of keeping LLM agents reliable and cost-efficient in production, structured as four mandatory layers: Context Engineering, Memory Architecture, Evaluation, and Observability & Guardrails. Every layer has specific implementation patterns — token budget allocation, memory type selection, golden dataset regression testing, and trace-span instrumentation — and skipping any layer creates a production liability. The non-negotiable principle is that developers must define correctness criteria for their domain before writing evals; AI tooling can implement but never substitute for that definitional work.

## Key Heuristics

These are the load-bearing rules for this concept.

> What is not in the context does not exist for the agent.

> More context is not always better — irrelevant context dilutes the signal and increases cost.

> LLMs pay more attention to the beginning and end of the context (primacy and recency effects). Put the most important information first and last.

> Skip any of these [4 layers], and your car becomes a liability.

> Can you write down on paper what 'correct' means for your system WITHOUT AI help? If not, you don't understand the problem yet.

> AI can help you implement evals, but YOU have to define what good looks like.

> Run evals every time you change the system.

> 10 requests/second × $0.01/request × 24 hours = $8,640/day. This happens to real companies.

## Anti-Patterns & Fixes

- Naive Context Stuffing: Concatenating all available context without token budgeting causes context window overflow, irrelevant signal dilution, and wasted cost. Fix: Use a ContextBuilder with explicit percentage budgets per component type and relevance-sorted truncation.
- Skipping Evals: Deploying without a golden dataset or defined correctness criteria means regressions and edge-case failures are discovered by users, not tests. Fix: Define what 'correct' means before deployment and run automated evals on every system change.
- AI-Generated Evals Without Human Ownership: Letting an LLM generate test cases without the developer understanding what is being tested produces a 90%-passing eval suite that misses real failure modes. Fix: The developer must define correctness criteria manually before using AI to expand test coverage.
- Amnesiac Agent (No Memory Architecture): Without persistent memory, every session starts from zero, making agents unable to reference prior interactions or user context. Fix: Implement all four memory types (in-context, episodic, semantic, procedural) appropriate to the use case.
- Unmonitored Production: Running agents without traces, cost tracking, or guardrails means failures are invisible until they cause user harm or budget overruns. Fix: Instrument every pipeline stage with spans, set cost budgets with hard stops, and attach input/output guardrail checks.

## When To Apply

Load this page when:

- Use this when building an agent that will make repeated LLM calls in production and you need to control token spend per request.
- Use this when a user's conversation history plus retrieved documents together risk exceeding the model's context window.
- Use this when an agent needs to reference information from previous sessions or remember user-specific facts across conversations.
- Use this when a production agent returns wrong, hallucinated, or out-of-scope outputs and you need to detect and block them automatically.
- Use this when you need to diagnose why an agent is slow and must isolate whether the bottleneck is retrieval, LLM latency, or guardrail processing.
- Use this when preparing to deploy an agent and you need to define a regression test suite that runs on every code or prompt change.
- Use this when costs are scaling unexpectedly and you need to route cheaper models for low-complexity queries.
- Use this when an agent handles sensitive user data and you must redact PII before it enters or exits the LLM.

## Concrete Examples

- Password reset query for 'Jane' (premium user): A 16,000-token budget is allocated across system prompt (200 tokens), user profile (50 tokens), retrieved docs (800 tokens), and conversation history (10 most recent messages), demonstrating context prioritization and budget arithmetic.
- ContextBuilder class with fit_docs and fit_history methods: Shows relevance-sorted doc inclusion with truncation fallback and recency-first history pruning in Python code.
- ContextCompressor with summarize_old_messages: Replaces old messages with a 3-5 bullet LLM-generated summary while keeping the N most recent messages verbatim.
- Full integrated agent run() method: Wires all 4 layers together — input guardrails, memory retrieval, context building, cost check, LLM generation, output guardrails, and memory storage — each wrapped in a named trace span.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**LLMOps Essentials**

An LLM coding agent generating agent infrastructure faces a specific failure mode: it will produce syntactically correct, plausible-looking eval suites and context builders without any grounding in what 'correct' actually means for the target domain, creating false confidence. The agent also cannot self-monitor costs or latency — without instrumented spans and budget checks baked into generated code, it will silently generate runaway-cost or slow pipelines with no observable signal. Critically, an LLM agent must treat context budget management as a first-class code constraint, not an afterthought, because it is itself subject to the same context window limits it is building around.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
