from openai import OpenAI

from app.config import settings
from app.tracing.tracer import Span

client = OpenAI(api_key=settings.openai_api_key)


def generate_embedding(text: str, span: Span | None = None) -> list[float]:
    response = client.embeddings.create(
        model=settings.embedding_model,
        input=text,
    )
    if span:
        span.model = settings.embedding_model
        usage = response.usage
        if usage:
            span.tokens_in = usage.prompt_tokens
            span.tokens_out = 0
    return response.data[0].embedding


def generate_embeddings(texts: list[str], span: Span | None = None) -> list[list[float]]:
    if not texts:
        return []
    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    if span:
        span.model = settings.embedding_model
        usage = response.usage
        if usage:
            span.tokens_in = usage.prompt_tokens
            span.tokens_out = 0
    return [item.embedding for item in response.data]
