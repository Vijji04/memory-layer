from fastapi import APIRouter

from app.models.memory import RetrieveRequest, RetrieveResponse
from app.services.embeddings import generate_embedding
from app.services.llm import generate_answer
from app.services.storage import search_long_term, search_session
from app.tracing.tracer import Trace

router = APIRouter()


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_memories(request: RetrieveRequest):
    trace = Trace()

    # Step 1: Embed the question
    with trace.span("query_embedding") as span:
        query_embedding = generate_embedding(request.question, span)

    # Step 2: Search both stores
    with trace.span("retrieval") as span:
        long_term_results = search_long_term(query_embedding, top_k=5)
        session_results = search_session(query_embedding, top_k=5)

        # Merge and sort by similarity
        all_results = long_term_results + session_results
        all_results.sort(key=lambda m: m.similarity_score, reverse=True)
        top_results = all_results[:5]

        span.metadata["long_term_hits"] = len(long_term_results)
        span.metadata["session_hits"] = len(session_results)
        span.metadata["total_returned"] = len(top_results)

    # Step 3: Generate answer using retrieved context
    with trace.span("response_generation") as span:
        if top_results:
            context_lines = []
            for i, mem in enumerate(top_results, 1):
                context_lines.append(
                    f"{i}. [{mem.memory_type}] (importance: {mem.importance}/10, "
                    f"similarity: {mem.similarity_score:.3f}, tier: {mem.tier}) "
                    f"{mem.fact}"
                )
            context = "\n".join(context_lines)
        else:
            context = "No relevant memories found."

        answer = generate_answer(request.question, context, span)

    return RetrieveResponse(
        retrieved_memories=top_results,
        answer=answer,
        trace=trace.to_dict(),
    )
