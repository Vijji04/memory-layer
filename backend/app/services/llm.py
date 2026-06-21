import json

from openai import OpenAI

from app.config import settings
from app.models.memory import (
    EvaluatedMemory,
    EvaluationResult,
    ExtractedFact,
    ExtractionResult,
)
from app.prompts.evaluation import (
    EVALUATION_RESPONSE_FORMAT,
    EVALUATION_SYSTEM_PROMPT,
    EVALUATION_USER_PROMPT,
)
from app.prompts.extraction import (
    EXTRACTION_RESPONSE_FORMAT,
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT,
)
from app.tracing.tracer import Span

client = OpenAI(api_key=settings.openai_api_key)


def extract_facts(text: str, span: Span) -> list[ExtractedFact]:
    span.model = settings.extraction_model
    response = client.chat.completions.create(
        model=settings.extraction_model,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": EXTRACTION_USER_PROMPT.format(text=text)},
        ],
        response_format=EXTRACTION_RESPONSE_FORMAT,
        temperature=0.2,
    )
    usage = response.usage
    if usage:
        span.tokens_in = usage.prompt_tokens
        span.tokens_out = usage.completion_tokens

    raw = json.loads(response.choices[0].message.content)
    result = ExtractionResult(**raw)
    return result.facts


def evaluate_memories(
    facts: list[ExtractedFact], span: Span
) -> list[EvaluatedMemory]:
    span.model = settings.evaluation_model
    candidates_json = json.dumps(
        [f.model_dump() for f in facts], indent=2
    )

    response = client.chat.completions.create(
        model=settings.evaluation_model,
        messages=[
            {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": EVALUATION_USER_PROMPT.format(
                    candidates_json=candidates_json
                ),
            },
        ],
        response_format=EVALUATION_RESPONSE_FORMAT,
        temperature=0.1,
    )
    usage = response.usage
    if usage:
        span.tokens_in = usage.prompt_tokens
        span.tokens_out = usage.completion_tokens

    raw = json.loads(response.choices[0].message.content)
    result = EvaluationResult(**raw)
    return result.memories


def generate_answer(question: str, context: str, span: Span) -> str:
    span.model = settings.response_model
    response = client.chat.completions.create(
        model=settings.response_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that answers questions using "
                    "the provided memory context. Always reference which memory "
                    "you used to form your answer. If no relevant memory is found, "
                    "say so honestly."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Retrieved memories:\n{context}\n\n"
                    f"Question: {question}"
                ),
            },
        ],
        temperature=0.3,
    )
    usage = response.usage
    if usage:
        span.tokens_in = usage.prompt_tokens
        span.tokens_out = usage.completion_tokens
    return response.choices[0].message.content
