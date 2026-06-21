from fastapi import APIRouter

from app.models.memory import (
    CaptureRequest,
    CaptureResponse,
    Decision,
    MemoryTier,
)
from app.services.embeddings import generate_embeddings
from app.services.llm import extract_facts, evaluate_memories
from app.services.storage import store_long_term_memory, store_session_memory
from app.tracing.tracer import Trace

router = APIRouter()


@router.post("/capture", response_model=CaptureResponse)
async def capture_memories(request: CaptureRequest):
    trace = Trace()

    # Stage 1: Extraction
    with trace.span("extraction") as span:
        facts = extract_facts(request.text, span)
        span.metadata["fact_count"] = len(facts)

    # Stage 2: Evaluation
    with trace.span("evaluation") as span:
        evaluated = evaluate_memories(facts, span)
        kept = [m for m in evaluated if m.decision == Decision.KEEP]
        dropped = [m for m in evaluated if m.decision == Decision.DROP]
        span.metadata["kept"] = len(kept)
        span.metadata["dropped"] = len(dropped)

    # Stage 3: Generate embeddings for kept memories
    stored = {"session": [], "long_term": []}
    if kept:
        with trace.span("embedding_generation") as span:
            texts = [m.fact for m in kept]
            embeddings = generate_embeddings(texts, span)
            span.metadata["count"] = len(texts)

        # Stage 4: Store to appropriate tier
        with trace.span("storage") as span:
            for memory, embedding in zip(kept, embeddings):
                if memory.tier == MemoryTier.SESSION:
                    store_session_memory(memory, embedding)
                    stored["session"].append(memory.fact)
                else:
                    store_long_term_memory(memory, embedding)
                    stored["long_term"].append(memory.fact)
            span.metadata["session_count"] = len(stored["session"])
            span.metadata["long_term_count"] = len(stored["long_term"])

    return CaptureResponse(
        extraction=facts,
        evaluation=evaluated,
        stored=stored,
        trace=trace.to_dict(),
    )
