# Agentic Memory Layer

A memory system for AI agents that captures, classifies, and retrieves facts from natural language — inspired by how ChatGPT's memory works under the hood.

Paste a paragraph containing multiple facts. The system extracts each one, classifies it by type and importance using an LLM-as-judge, routes it to the right store (session or long-term), and lets you query it back with semantic search and explainable retrieval signals.

---

## What It Does

**Feature 1 — Capture & Classify (write path)**

A multi-stage pipeline that processes raw text into structured, classified memories:

```
"I prefer Python over Java. My current project uses FastAPI.
 I had a sandwich for lunch. Always use type hints."
                            │
                            ▼
               ┌────────────────────────┐
               │   Extraction Agent     │
               │   (GPT-4o, temp=0.2)   │
               │                        │
               │  Pulls out each fact   │
               │  as a separate entry   │
               └───────────┬────────────┘
                           │
          ┌────────────────┴────────────────┐
          │  Candidate 1: "Prefers Python"  │
          │  Candidate 2: "Uses FastAPI"    │
          │  Candidate 3: "Had sandwich"    │
          │  Candidate 4: "Use type hints"  │
          └────────────────┬────────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │   Evaluator (Judge)    │
               │   (GPT-4o, temp=0.1)   │
               │                        │
               │  For each candidate:   │
               │  • type: semantic /    │
               │    episodic /          │
               │    procedural          │
               │  • importance: 1-10    │
               │  • confidence: 0-1     │
               │  • decision: keep/drop │
               │  • tier: session /     │
               │    long_term           │
               │  • reason: "..."       │
               └───────────┬────────────┘
                           │
          ┌────────────────┴────────────────┐
          │  ✓ KEEP "Prefers Python"        │
          │    semantic, importance 8,       │
          │    long_term                     │
          │  ✓ KEEP "Uses FastAPI"           │
          │    semantic, importance 6,       │
          │    session                       │
          │  ✗ DROP "Had sandwich"           │
          │    episodic, importance 2        │
          │  ✓ KEEP "Use type hints"         │
          │    procedural, importance 7,     │
          │    long_term                     │
          └────────────────┬────────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │   Embedding + Storage  │
               │                        │
               │  text-embedding-3-small│
               │  → 1536-dim vectors    │
               │                        │
               │  session → in-memory   │
               │  long_term → Postgres  │
               └────────────────────────┘
```

**Feature 2 — Retrieve & Explain (read path)**

Ask a question. The system searches both memory stores, returns the top matches with similarity scores and retrieval signals, then generates an answer grounded in retrieved context.

```
"What language do I prefer?"
            │
            ▼
   ┌──────────────────┐
   │  Embed question   │
   │  (same model)     │
   └────────┬─────────┘
            │
     ┌──────┴──────┐
     ▼              ▼
┌──────────┐  ┌──────────┐
│ Session  │  │ Long-term│
│  Store   │  │  Store   │
│(in-memory)│ │(Postgres)│
└────┬─────┘  └────┬─────┘
     │              │
     └──────┬───────┘
            │
            ▼
   ┌──────────────────┐
   │  Rank by cosine   │
   │  similarity       │
   │  + build signal   │
   └────────┬─────────┘
            │
            ▼
  "semantic similarity: 0.921
   | high importance (8/10)"
            │
            ▼
   ┌──────────────────┐
   │  Response LLM    │
   │  (GPT-4o)        │
   │                   │
   │  Answer grounded  │
   │  in retrieved     │
   │  memories         │
   └──────────────────┘
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend                          │
│              Next.js + Tailwind CSS                  │
│                                                      │
│  ┌──────────────┐           ┌──────────────────┐    │
│  │ CapturePanel │           │  RetrievePanel   │    │
│  │              │           │                  │    │
│  │  textarea    │           │  question input  │    │
│  │  → stages    │           │  → memories      │    │
│  │  → storage   │           │  → answer        │    │
│  │  → trace     │           │  → trace         │    │
│  └──────┬───────┘           └────────┬─────────┘    │
│         │                            │               │
│         └────────────┬───────────────┘               │
│                      │ HTTP (JSON)                   │
└──────────────────────┼───────────────────────────────┘
                       │
┌──────────────────────┼───────────────────────────────┐
│                  Backend                              │
│               FastAPI (Python)                        │
│                      │                               │
│         ┌────────────┴────────────┐                  │
│         │                         │                  │
│  POST /api/capture        POST /api/retrieve         │
│         │                         │                  │
│    ┌────┴─────┐             ┌─────┴────┐            │
│    │ Services │             │ Services │            │
│    │          │             │          │            │
│    │ extract  │             │ embed    │            │
│    │ evaluate │             │ search   │            │
│    │ embed    │             │ generate │            │
│    │ store    │             │          │            │
│    └────┬─────┘             └─────┬────┘            │
│         │                         │                  │
│    ┌────┴─────────────────────────┴────┐            │
│    │           Tracing Layer           │            │
│    │  Spans: latency, tokens, model,   │            │
│    │  metadata per pipeline stage      │            │
│    └───────────────────────────────────┘            │
│                      │                               │
└──────────────────────┼───────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────┴───┐   ┌─────┴────┐  ┌────┴────┐
    │ OpenAI │   │ Postgres │  │ Session │
    │  API   │   │ +pgvector│  │  Store  │
    │        │   │          │  │(in-mem) │
    │ GPT-4o │   │ long-term│  │ session │
    │ embed  │   │ memories │  │memories │
    └────────┘   └──────────┘  └─────────┘
```

---

## Memory Classification System

The evaluator classifies memories using a psychological model:

| Type | Definition | Examples | UI Color |
|------|-----------|----------|----------|
| **Semantic** | General truths, preferences, beliefs, enduring facts | "I prefer Python over Java", "PostgreSQL is the best relational DB" | Emerald |
| **Episodic** | Specific events, time-bound occurrences | "I had coffee this morning", "We shipped v2 last Tuesday" | Cyan |
| **Procedural** | Rules, processes, instructions, how-tos | "Always use type hints in Python", "Deploy with docker compose up" | Violet |

### Scoring

| Field | Range | Purpose |
|-------|-------|---------|
| `importance` | 1–10 | How useful for future interactions. >= 4 = keep, < 4 = drop |
| `confidence` | 0–1 | LLM's confidence in its own classification |
| `tier` | session / long_term | session = current project scope, long_term = durable preference |

Tier reflects **scope**, not lifetime management. Session-tier facts are things true for the current project; long-term facts are recurring and durable. No decay or expiry logic — just routing at write time.

---

## Tech Stack

### Backend
| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.115.6 |
| LLM | OpenAI GPT-4o (extraction, evaluation, response) |
| Embeddings | OpenAI text-embedding-3-small (1536 dims) |
| Database | PostgreSQL 16 + pgvector 0.8.3 |
| ORM | SQLAlchemy 2.0.36 |
| Session store | In-memory Python dict |
| Similarity | NumPy cosine similarity |
| Tracing | Custom span-based tracer (returned in API response) |

### Frontend
| Component | Technology |
|-----------|-----------|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript 5 |
| Styling | Tailwind CSS 4 |
| Fonts | Geist Sans + Geist Mono |

### Infrastructure
| Component | Technology |
|-----------|-----------|
| Database | Docker (pgvector/pgvector:pg16) |
| Backend deploy | Render / Railway |
| Frontend deploy | Vercel |

---

## API Reference

### `POST /api/capture`

Process text into classified memories.

**Request:**
```json
{
  "text": "I prefer Python over Java. My current project uses FastAPI. I had a sandwich for lunch. Always use type hints in Python."
}
```

**Response:**
```json
{
  "extraction": [
    {
      "fact": "Prefers Python over Java for backend work",
      "source_sentence": "I prefer Python over Java."
    }
  ],
  "evaluation": [
    {
      "fact": "Prefers Python over Java for backend work",
      "source_sentence": "I prefer Python over Java.",
      "type": "semantic",
      "importance": 8,
      "confidence": 0.95,
      "decision": "keep",
      "tier": "long_term",
      "reason": "Durable language preference useful for future recommendations"
    }
  ],
  "stored": {
    "session": ["Current project uses FastAPI"],
    "long_term": ["Prefers Python over Java", "Always use type hints in Python"]
  },
  "trace": {
    "trace_id": "a4c9e0c72301",
    "total_duration_ms": 3847.21,
    "total_tokens_in": 1523,
    "total_tokens_out": 412,
    "spans": [
      {
        "name": "extraction",
        "duration_ms": 1200.5,
        "tokens_in": 380,
        "tokens_out": 195,
        "model": "gpt-4o"
      },
      {
        "name": "evaluation",
        "duration_ms": 1800.3,
        "tokens_in": 920,
        "tokens_out": 217,
        "model": "gpt-4o"
      },
      {
        "name": "embedding_generation",
        "duration_ms": 450.1,
        "tokens_in": 45,
        "tokens_out": 0,
        "model": "text-embedding-3-small"
      },
      {
        "name": "storage",
        "duration_ms": 12.3,
        "tokens_in": 0,
        "tokens_out": 0,
        "model": ""
      }
    ]
  }
}
```

### `POST /api/retrieve`

Search stored memories and generate an answer.

**Request:**
```json
{
  "question": "What programming language do I prefer?"
}
```

**Response:**
```json
{
  "retrieved_memories": [
    {
      "id": "f01bc4a15355",
      "fact": "Prefers Python over Java for backend work",
      "memory_type": "semantic",
      "importance": 8,
      "confidence": 0.95,
      "tier": "long_term",
      "similarity_score": 0.9214,
      "signal": "semantic similarity: 0.921 | high importance (8/10)"
    }
  ],
  "answer": "Based on your stored preferences, you prefer Python over Java for backend work. This was classified as a strong, durable preference (importance 8/10).",
  "trace": { "..." }
}
```

### `GET /health`

```json
{"status": "ok"}
```

---

## Observability

Every API call returns a `trace` object with full pipeline visibility:

```
┌─ Trace: a4c9e0c72301 ─ 3847ms ─ 1935 tokens ──────────┐
│                                                          │
│  extraction        ████████████░░░░░░░░  1200ms  gpt-4o │
│  evaluation        ██████████████████░░  1800ms  gpt-4o │
│  embedding_gen     █████░░░░░░░░░░░░░░░   450ms  embed  │
│  storage           █░░░░░░░░░░░░░░░░░░░    12ms         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

Each span captures:
- **name** — pipeline stage
- **duration_ms** — wall-clock time
- **tokens_in / tokens_out** — token usage per LLM call
- **model** — which model was used
- **metadata** — stage-specific data (fact_count, kept/dropped, hit counts)
- **error** — error message if the span failed

The frontend renders this as an expandable trace panel with proportional duration bars.

---

## Project Structure

```
agentic-memory-layer/
│
├── backend/                        # FastAPI backend (deploy to Render/Railway)
│   ├── Dockerfile
│   ├── docker-compose.yml          # PostgreSQL + pgvector (local dev)
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       ├── main.py                 # App setup, CORS, error handling, lifespan
│       ├── config.py               # Settings from environment variables
│       ├── api/
│       │   ├── capture.py          # POST /api/capture — write path
│       │   └── retrieve.py         # POST /api/retrieve — read path
│       ├── services/
│       │   ├── llm.py              # OpenAI calls: extract, evaluate, answer
│       │   ├── embeddings.py       # text-embedding-3-small embeddings
│       │   └── storage.py          # PostgreSQL + in-memory session store
│       ├── models/
│       │   └── memory.py           # Pydantic schemas (request/response/domain)
│       ├── prompts/
│       │   ├── extraction.py       # Extraction agent system + user prompts
│       │   └── evaluation.py       # Evaluator (LLM-as-judge) prompts
│       └── tracing/
│           └── tracer.py           # Span-based tracing (returned in responses)
│
└── frontend/                       # Next.js frontend (deploy to Vercel)
    ├── package.json
    ├── next.config.ts
    ├── tsconfig.json
    ├── .env.local
    └── src/
        ├── app/
        │   ├── layout.tsx          # Root layout, dark theme, Geist fonts
        │   ├── page.tsx            # Tab navigation: Capture | Retrieve
        │   └── globals.css         # Tailwind config, scrollbar, code blocks
        ├── components/
        │   ├── CapturePanel.tsx    # Write path UI (stages + storage + trace)
        │   ├── RetrievePanel.tsx   # Read path UI (memories + answer + trace)
        │   └── TracePanel.tsx      # Expandable trace visualization
        └── lib/
            └── api.ts              # Typed API client with error handling
```

---

## Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker (for PostgreSQL + pgvector)
- OpenAI API key with GPT-4o access

### 1. Clone

```bash
git clone https://github.com/<your-username>/agentic-memory-layer.git
cd agentic-memory-layer
```

### 2. Start the database

```bash
cd backend
docker compose up -d
```

This starts PostgreSQL 16 with pgvector on port **5433** (remapped to avoid conflicts with local Postgres).

### 3. Configure the backend

```bash
cp .env.example .env
```

Edit `.env` and set your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/memory_layer
CORS_ORIGINS=["http://localhost:3000"]
```

### 4. Install and start the backend

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs at `http://localhost:8000`. Verify with:

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

### 5. Install and start the frontend

```bash
cd ../frontend
npm install
```

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the dev server:

```bash
npm run dev
```

Open `http://localhost:3000`.

---

## Deployment

The production stack is **Neon** (database) + **Railway** (backend) + **Vercel** (frontend).

```
┌──────────┐       ┌──────────┐       ┌──────────┐
│  Vercel  │──────▶│ Railway  │──────▶│   Neon   │
│ (Next.js)│ HTTP  │(FastAPI) │  SQL  │(Postgres)│
└──────────┘       └──────────┘       └──────────┘
```

### 1. Database → Neon

[Neon](https://neon.tech) provides serverless PostgreSQL with pgvector on the free tier.

1. Create a Neon account and project
2. The default database `neondb` works fine
3. Copy the connection string from the dashboard — it looks like:
   ```
   postgresql://user:pass@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. In the Neon SQL editor, enable pgvector (optional — not required for current implementation but good to have):
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

### 2. Backend → Railway

[Railway](https://railway.com) deploys Docker containers with no cold starts.

1. Push your repo to GitHub
2. Create a new project on Railway → **Deploy from GitHub repo**
3. Set the **root directory** to `backend/`
4. Railway auto-detects the Dockerfile
5. Add environment variables in Railway's dashboard:

   | Variable | Value |
   |----------|-------|
   | `OPENAI_API_KEY` | `sk-your-key` |
   | `DATABASE_URL` | Neon connection string from step 1 |
   | `CORS_ORIGINS` | `["https://your-app.vercel.app"]` |

6. Railway assigns a public URL (e.g., `https://your-app.up.railway.app`)
7. Deploy

The `PORT` env var is set automatically by Railway — the Dockerfile reads it.

### 3. Frontend → Vercel

1. Import the same repo in [Vercel](https://vercel.com)
2. Set the **root directory** to `frontend/`
3. Add environment variable:

   | Variable | Value |
   |----------|-------|
   | `NEXT_PUBLIC_API_URL` | Your Railway backend URL (e.g., `https://your-app.up.railway.app`) |

4. Deploy

### After deploying

Go back to Railway and update `CORS_ORIGINS` to match the actual Vercel URL if it differs from what you initially set.

---

## Design Decisions

### Why two separate LLM calls (extraction + evaluation)?

The pipeline is split into two stages intentionally — not for engineering reasons, but for **demo visibility**. Showing the raw extracted facts separately from the classification makes the keep/drop split and the session/long-term routing obvious at a glance. A single combined call would work but hide the intermediate reasoning.

### Why in-memory dict for session store instead of Redis?

For a demo, an in-memory dict is the simplest possible session store — zero dependencies, instant read/write. Session memories are scoped to the current server process and cleared on restart, which is acceptable for demo purposes. Swap to Redis for production persistence.

### Why cosine similarity in Python instead of pgvector operators?

The storage layer serializes embeddings as JSON text and computes similarity in Python with NumPy. This avoids requiring pgvector SQL operators and keeps the storage layer simple. For production scale (thousands+ of memories), swap to pgvector's native `<=>` cosine distance operator with an IVFFlat or HNSW index.

### Why structured output (JSON schema mode)?

Both the extraction and evaluation prompts use OpenAI's `response_format` with strict JSON schemas. This guarantees parseable output on every call — no regex parsing, no retry-on-malformed-JSON. The trade-off is slightly higher latency, but reliability matters more for a demo.

### Why trace data in the API response instead of a separate observability tool?

For a hackathon demo, embedding trace data directly in the response makes it immediately visible in the UI. No separate dashboard, no log aggregation, no Langfuse setup. The frontend renders latency bars, token counts, and model names inline. For production, add OpenTelemetry export alongside the response-embedded traces.

### Temperature tuning

| Stage | Temperature | Reasoning |
|-------|------------|-----------|
| Extraction | 0.2 | Precise fact-pulling, minimal hallucination |
| Evaluation | 0.1 | Consistent classification across runs |
| Response | 0.3 | Slightly more natural language in answers |

### What's not included (and why)

| Omitted | Reason |
|---------|--------|
| Hybrid retrieval (BM25 + dense) | Cosine similarity alone is sufficient at demo scale |
| Memory decay / expiry | Tier is routing, not lifecycle — no decay logic needed |
| Auth / RBAC | No trust boundary in demo scope |
| Shadow mode / canary | Not deploying to production users |
| Guardrail layer | No untrusted external input |
| CI/CD pipeline | Single deploy, no continuous delivery needed |

---

## How the Retrieval Signal Works

When a memory is retrieved, the system builds a human-readable **signal** explaining why it matched:

```
"semantic similarity: 0.921 | high importance (8/10)"
```

The signal combines:
1. **Cosine similarity** — how close the question embedding is to the memory embedding
2. **Importance level** — flagged if importance >= 7 ("high") or >= 4 ("moderate")

This makes retrieval transparent — users can see *why* a particular memory was surfaced, not just *that* it was.

---

## License

MIT
